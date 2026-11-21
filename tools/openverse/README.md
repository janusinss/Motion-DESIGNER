# Openverse API Client (`tools/openverse/`)

Minimal Python standard-library client and live connectivity check for the [Openverse API v1](https://api.openverse.org/v1/) (Creative Commons images and audio).

## Requirements

- Python 3.9+ (uses only standard library: `urllib`, `json`, `argparse`).
- Internet access to `https://api.openverse.org/v1/`.

## Usage

### Verify Connectivity (Images + Audio)

```powershell
python tools/openverse/openverse_client.py --check --limit 1
```

### Search Images or Audio

```powershell
# Search CC images
python tools/openverse/openverse_client.py --type images -q "abstract geometric" -n 5

# Search CC0 audio
python tools/openverse/openverse_client.py --type audio -q "ambient synth" --license cc0 -n 3

# Raw JSON output
python tools/openverse/openverse_client.py --type images -q "kinetic" -n 2 --json
```

## Notes

- Anonymous requests are rate-limited by Openverse. Always review item `license` and `attribution` fields before using retrieved assets.
