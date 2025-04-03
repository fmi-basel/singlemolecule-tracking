# Train Model

## Build Config
```commandline
WD=runs/example pixi run build_config
```

## Submit Job

### Option 1: Run it locally
```commandline
WD=runs/example pixi run train
```

### Option2: Run it on a cluster
```commandline
WD=runs/example JOB=train ACCOUNT=account-name pixi run submit_job
```
Replace `account-name` with your cluster account name.
