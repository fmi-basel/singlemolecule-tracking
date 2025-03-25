# Train Model

## Build Config
```commandline
WD=runs/example pixi run build_config
```

## Submit Job
```commandline
WD=runs/example JOB=train ACCOUNT=account-name pixi run submit_job
```
Replace `account-name` with your cluster account name.
