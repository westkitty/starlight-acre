#!/bin/bash
set -eu

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SELF_DIR/.." && pwd)"
GODOT_BIN="${GODOT:-}"

if [ -z "$GODOT_BIN" ]; then
	GODOT_BIN="$(command -v godot 2>/dev/null || command -v godot4 2>/dev/null || true)"
fi
if [ -z "$GODOT_BIN" ] || [ ! -x "$GODOT_BIN" ]; then
	echo "STARLIGHT_CORE_TEST_FAIL: Godot 4 executable not found." >&2
	exit 1
fi

QA_HOME="$(mktemp -d "${TMPDIR:-/tmp}/starlight-core-tests.XXXXXX")"
cleanup() {
	case "$QA_HOME" in
		*/starlight-core-tests.*) python3 -c 'import shutil,sys; shutil.rmtree(sys.argv[1], ignore_errors=True)' "$QA_HOME" ;;
	esac
}
trap cleanup EXIT

run_godot() {
	env HOME="$QA_HOME" "$GODOT_BIN" "$@"
}

run_expect() {
	token="$1"
	shift
	log="$QA_HOME/$token.log"
	if ! run_godot "$@" >"$log" 2>&1; then
		cat "$log"
		echo "STARLIGHT_CORE_TEST_FAIL: Godot process failed before $token" >&2
		exit 1
	fi
	cat "$log"
	if grep -Eq 'SCRIPT ERROR:|(^| )ERROR:' "$log"; then
		echo "STARLIGHT_CORE_TEST_FAIL: Godot emitted errors before $token" >&2
		exit 1
	fi
	if ! grep -q "$token" "$log"; then
		echo "STARLIGHT_CORE_TEST_FAIL: missing required token $token" >&2
		exit 1
	fi
}

echo "[1/5] Checking Godot import cache"
if [ ! -f "$REPO_ROOT/.godot/global_script_class_cache.cfg" ] || [ ! -f "$REPO_ROOT/assets/backgrounds/greenhouse_sector_bg.png.import" ]; then
	echo "  Fresh checkout detected; priming Godot imports"
	if ! run_godot --headless --editor --path "$REPO_ROOT" --quit >"$QA_HOME/import.log" 2>&1; then
		cat "$QA_HOME/import.log"
		exit 1
	fi
else
	echo "  Import cache already ready"
fi

echo "[2/5] Writing persistence fixture"
run_expect STARLIGHT_PERSISTENCE_WRITE_PASS --headless --path "$REPO_ROOT" --script res://tests/persistence_write_test.gd

echo "[3/5] Relaunching and reading persistence fixture"
run_expect STARLIGHT_PERSISTENCE_READ_PASS --headless --path "$REPO_ROOT" --script res://tests/persistence_read_test.gd

echo "[4/5] Running core system integration checks"
run_expect STARLIGHT_CORE_SYSTEMS_PASS --headless --path "$REPO_ROOT" --script res://tests/core_systems_test.gd

echo "[5/5] Running configured main scene for 120 frames"
main_log="$QA_HOME/main_scene.log"
if ! run_godot --headless --path "$REPO_ROOT" --quit-after 120 >"$main_log" 2>&1; then
	cat "$main_log"
	echo "STARLIGHT_CORE_TEST_FAIL: configured main scene process failed" >&2
	exit 1
fi
cat "$main_log"
if grep -Eq '(^| )ERROR:|SCRIPT ERROR:' "$main_log"; then
	echo "STARLIGHT_CORE_TEST_FAIL: configured main scene emitted runtime errors" >&2
	exit 1
fi

echo "STARLIGHT_CORE_TEST_SUITE_PASS"
