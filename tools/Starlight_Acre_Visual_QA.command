#!/bin/bash
#
# Starlight Acre — One-Click Visual QA (macOS)
#
# Double-click this file in Finder. It will:
#   1. Find Godot on this Mac (nothing is downloaded or installed).
#   2. Run the project's two technical checks (asset promotion test + smoke test).
#   3. Briefly open the game window and capture real screenshots of the
#      Greenhouse and Engineering sectors, plus close-up QA crops of the
#      player frames, Wisdom Fruit states, terminals and HUD icons.
#   4. Build an offline HTML review report.
#   5. Open the report in your browser.
#
# Results land in  visual_qa_output/  at the repository root (not committed).
# Previous QA results are replaced on each run.
#
# Safety: the game, its artwork, and your real saves are never modified.
# Every Godot run uses an isolated HOME folder inside visual_qa_output/,
# so the QA run cannot read or write your actual Godot application data.
#
# Requirements: macOS, Godot 4.x (4.7.1 verified), python3.

set -u

# ------------------------------------------------------------------ progress UI

say()  { printf '\n%s\n' "$1"; }
step() { printf '\n%s %s\n' "$1" "$2"; }

hold_window() {
	printf '\nPress RETURN to close this window (or just close it)...'
	IFS= read -r _reply 2>/dev/null || true
	printf '\n'
}

die() {
	printf '\n%s\n' "$1" >&2
	hold_window
	exit 1
}

# ---------------------------------------------------------- 1. locate repository

SELF="${BASH_SOURCE[0]:-$0}"
TOOLS_DIR=""
REPO_ROOT=""
TOOLS_DIR="$(cd "$(dirname "$SELF")" && pwd 2>/dev/null)" || TOOLS_DIR=""
if [ -n "$TOOLS_DIR" ]; then
	REPO_ROOT="$(cd "$TOOLS_DIR/.." && pwd 2>/dev/null)" || REPO_ROOT=""
fi
if [ -z "$REPO_ROOT" ] || [ ! -f "$REPO_ROOT/project.godot" ]; then
	die "This launcher must stay inside the Starlight Acre repository (in the
tools/ folder). It could not find project.godot one level up, so it cannot run.

Location of this file: ${SELF:-unknown}"
fi

# ------------------------------------------------------------- 2. find Godot 4

step "[1/5]" "Looking for Godot..."

godot_candidates() {
	command -v godot 2>/dev/null || true
	command -v godot4 2>/dev/null || true
	command -v godot-mono 2>/dev/null || true
	for _p in /usr/local/bin/godot /usr/local/bin/godot4 /opt/homebrew/bin/godot /opt/homebrew/bin/godot4; do
		[ -x "$_p" ] && printf '%s\n' "$_p"
	done
	for _app in /Applications/Godot*.app "$HOME"/Applications/Godot*.app; do
		if [ -d "$_app" ] && [ -x "$_app/Contents/MacOS/Godot" ]; then
			printf '%s\n' "$_app/Contents/MacOS/Godot"
		fi
	done
	true
}

GODOT=""
GODOT_VERSION=""
REJECTED=""
while IFS= read -r _cand; do
	[ -z "$_cand" ] && continue
	_ver="$("$_cand" --version 2>/dev/null | head -n 1)"
	case "$_ver" in
		4*) GODOT="$_cand"; GODOT_VERSION="$_ver"; break ;;
		*)  REJECTED="${REJECTED}  - ${_cand}  (reported version: ${_ver:-no version})\n" ;;
	esac
done <<EOF
$(godot_candidates)
EOF

if [ -z "$GODOT" ]; then
	if [ -n "$REJECTED" ]; then
		_rej="$(printf '%b' "$REJECTED")"
		die "Godot was found, but it is not version 4.x, which Starlight Acre
needs (4.7.1 is the verified version).

Found:
${_rej}

Please install the Godot 4 app (for example, put Godot.app in /Applications)
and double-click this file again."
	else
		die "Godot could not be found on this Mac.

The visual QA harness needs the Godot app to run the game and take
screenshots. Nothing was downloaded or installed.

Places that were checked:
  - the godot / godot4 / godot-mono terminal commands
  - /usr/local/bin and /opt/homebrew/bin
  - /Applications/Godot*.app
  - the Applications folder in your home folder

To fix this: install the Godot 4 app (drag Godot.app into /Applications),
then double-click this file again."
	fi
fi
printf '  Found Godot %s\n  %s\n' "$GODOT_VERSION" "$GODOT"

# --------------------------------------------------------------- 3. find python3

if command -v python3 >/dev/null 2>&1; then
	PYTHON="$(command -v python3)"
	printf '  Found python3: %s\n' "$PYTHON"
else
	die "python3 could not be found. macOS normally includes it (it comes with
Apple's Command Line Tools). Install those once, then double-click this file
again. No other software is needed."
fi

# ------------------------------------------------------------ 4. prepare output

OUT_DIR="$REPO_ROOT/visual_qa_output"
QA_HOME="$OUT_DIR/.qa_home"

case "$OUT_DIR" in
	*/visual_qa_output) ;;           # expected shape — safe to rebuild below
	*) die "Refusing to continue: unexpected output path '$OUT_DIR'." ;;
esac

step "[2/5]" "Preparing the output folder (previous QA results are replaced)"
rm -rf "$OUT_DIR" 2>/dev/null
mkdir -p "$OUT_DIR" 2>/dev/null || die "Could not create the output folder:
$OUT_DIR"
mkdir -p "$QA_HOME" 2>/dev/null || die "Could not create the temporary QA folder:
$QA_HOME"
printf '  %s\n' "$OUT_DIR"

# Run Godot with an isolated HOME so the QA run cannot read or write the
# user's real Godot application data (real saves stay untouched).
run_godot() {
	env HOME="$QA_HOME" "$GODOT" "$@"
}

# Run a command with a watchdog so a stuck process can never hang forever.
run_with_timeout() {
	_secs="$1"
	shift
	"$@" &
	_pid=$!
	( sleep "$_secs" && kill -TERM "$_pid" 2>/dev/null ) &
	_watchdog=$!
	wait "$_pid"
	_rc=$?
	kill -TERM "$_watchdog" 2>/dev/null
	wait "$_watchdog" 2>/dev/null
	return "$_rc"
}

# --------------------------------------------------- 5. prime Godot imports

printf '\n  Preparing Godot imports for this checkout...\n'
printf 'godot --headless --editor --path <repo> --quit\n\n' > "$OUT_DIR/check_import.log"
if run_with_timeout 180 run_godot --headless --editor --path "$REPO_ROOT" --quit >> "$OUT_DIR/check_import.log" 2>&1; then
	printf '  Godot import cache: ready\n'
else
	_import_rc=$?
	printf '  Godot import cache: FAILED (exit %s)\n' "$_import_rc"
	die "Godot could not finish importing this checkout. Details are saved in:\n$OUT_DIR/check_import.log"
fi

# ------------------------------------------------------- 6. technical checks

step "[3/5]" "Running technical checks (no game window opens for this)"

run_check() {
	_name="$1"
	_script="$2"
	_token="$3"
	_log="$OUT_DIR/check_${_name}.log"
	_rcfile="$OUT_DIR/check_${_name}.rc"
	printf 'godot --headless --path <repo> --script %s\n\n' "$_script" > "$_log"
	if run_with_timeout 90 run_godot --headless --path "$REPO_ROOT" --script "$_script" >> "$_log" 2>&1; then
		printf '0' > "$_rcfile"
	else
		printf '%s' "$?" > "$_rcfile"
	fi
	_rc_val="$(cat "$_rcfile" 2>/dev/null)"
	if [ "$_rc_val" -ge 124 ] 2>/dev/null; then
		printf '\n[launcher] check timed out after 90 seconds and was stopped\n' >> "$_log"
	fi
	if [ "$_rc_val" = "0" ] && grep -q "$_token" "$_log"; then
		printf '  %s: PASS\n' "$_name"
	else
		printf '  %s: FAIL  (details will be shown in the report)\n' "$_name"
	fi
}

run_check "asset_test" "res://tests/asset_promotion_test.gd" "STARLIGHT_ASSET_PROMOTION_PASS"
run_check "smoke_test" "res://tests/smoke_test.gd" "STARLIGHT_SMOKE_PASS"

# --------------------------------------------------------- 6. capture screenshots

step "[4/5]" "Capturing screenshots (a game window opens for a few seconds —
please leave it alone until it closes by itself)"

printf 'godot --path <repo> --script res://tools/visual_qa/run_visual_qa.gd\n\n' > "$OUT_DIR/check_capture.log"
if run_with_timeout 90 run_godot --path "$REPO_ROOT" --audio-driver Dummy --script "res://tools/visual_qa/run_visual_qa.gd" >> "$OUT_DIR/check_capture.log" 2>&1; then
	printf '0' > "$OUT_DIR/check_capture.rc"
else
	printf '%s' "$?" > "$OUT_DIR/check_capture.rc"
fi
_rc_val="$(cat "$OUT_DIR/check_capture.rc" 2>/dev/null)"
if [ "$_rc_val" -ge 124 ] 2>/dev/null; then
	printf '\n[launcher] capture timed out after 90 seconds and was stopped\n' >> "$OUT_DIR/check_capture.log"
fi
for _shot in greenhouse.png engineering.png; do
	if [ -s "$OUT_DIR/$_shot" ]; then
		printf '  %s: captured\n' "$_shot"
	else
		printf '  %s: MISSING (this will be shown in the report)\n' "$_shot"
	fi
done

# Record which commit is being reviewed (best effort).
git -C "$REPO_ROOT" rev-parse --short HEAD > "$OUT_DIR/git_commit.txt" 2>/dev/null || printf 'unknown' > "$OUT_DIR/git_commit.txt"

# --------------------------------------------------------------- 7. build report

step "[5/5]" "Building the visual QA report"
if ! "$PYTHON" "$REPO_ROOT/tools/visual_qa/build_report.py" --repo "$REPO_ROOT" --output "$OUT_DIR" > "$OUT_DIR/build_report.log" 2>&1; then
	cat "$OUT_DIR/build_report.log" >&2
	die "Building the QA report failed. The messages above (also saved in
$OUT_DIR/build_report.log) may explain why."
fi
tail -n 2 "$OUT_DIR/build_report.log" 2>/dev/null

# The isolated QA HOME is no longer needed — it lives inside visual_qa_output/
# and never touched real user data.
rm -rf "$QA_HOME"

# ------------------------------------------------------------------ 8. open it

if command -v open >/dev/null 2>&1 && open "$OUT_DIR/index.html"; then
	say "The Starlight Acre visual QA report should now be open in your browser."
else
	say "The report is ready — open this file in your browser:
$OUT_DIR/index.html"
fi
say "Review each section (LOOKS GOOD / NEEDS ATTENTION), add notes where
needed, press SHOW REVIEW SUMMARY, and copy the text back to the chat."
printf '\nAll done. This window can be closed.\n'
exit 0
