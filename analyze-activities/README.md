# analyze-activities

activity data from different hobbies/source are converted into a common json format:
key: date, value=list(title)

```json
{
  "2025-01-01": [
    "00:00 New Year",
    "09:47 Wake up",
    "09:34 Jogging in the Snow (65 min)",
    "Some text without a time."
  ]
}
```

## Calender appointments

1. export your calendar in ics format to `data/cal.ics`
2. run [cal.py](src/cal.py) to convert into `output/cal.json`

format: `HH:MM TITLE`

## Git commits

Assuming all your local git repositories are in the same directory that this clone.

1. run [git_1_export_history.sh](src/git_1_export_history.sh) to extract commit data from all local repos to `data/git/*.log`
2. run [git_2.py](src/git_2.py) to convert into `output/git.json`

format: `HH:MM Coding at REPO: COMMIT_TITLE`

## LifeLog (Diary/Journal)

If you write a free text diary.

1. copy/paste from source document to `data/lifelog.md`
2. run [lifelog.py](src/lifelog.py) to convert into `output/lifelog.json`

## Oura ring sleep times

If you have an [Oura ring](https://ouraring.com) device, to measure you sleep.

1. download [sleep.csv](https://cloud.ouraring.com/account/export/sleep/csv) to `data/oura/sleep.csv`
2. or use my [Oura download script](https://github.com/entorb/analyze-oura)
3. run [oura.py](src/oura.py) to convert into `output/oura.json`

format: `HH:MM Start sleep` and `HH:MM Wake up`

## Strava activities

If you are using [Strava](https://www.strava.com) to share you sports activities.

1. export ics list of activities via my [Strava analysis app](https://entorb.net/strava-streamlit/) -> "Cal Export" to `data/strava/Strava_Activity_Calendar.ics`
2. run [strava.py](src/strava.py) to convert into `output/strava.json`

format: `HH:MM TYPE: TITLE (MINUTES)`

## Remember the Milk (To-do list)

If you are organizing your tasks via [Remember the Milk](https://www.rememberthemilk.com).

1. from my [rememberthemilk](https://github.com/entorb/rememberthemilk/) repo, run [tasks_completed.py](https://github.com/entorb/rememberthemilk/blob/main/src/tasks_completed.py)
2. copy/pase from source to `data/rtm_tasks_completed.csv`
3. run [rtm.py](src/rtm.py) to convert into `output/rtm.json`

format: `HH:MM Task LIST: TITLE (ESTIMATION)`

## Join all

run [join.py](src/join.py) to generate `output/join.json`

## Run all

run [run-all.sh](src/run-all.sh) to do all in one step

## Tools

### Pytest unit tests

```sh
uv run pytest tests/ --cov --cov-report=html:coverage_report
```

### Ruff formatter and linter

```sh
uv run ruff format
uv run ruff check --fix
```

### Pre-commit code checker

(also runs Ruff and CSpell)

```sh
uv run pre-commit run --all-files
```

### SonarQube Code Analysis

See report at [sonarcloud.io](https://sonarcloud.io/summary/overall?id=entorb_analyze-activities&branch=main)
