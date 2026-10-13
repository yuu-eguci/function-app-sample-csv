# TimerTrigger - Python

`TimerTrigger` で、この関数を 1 分ごとに実行する。実行のたびに `jason_statham.csv` を読んで、件数と各行をログに出す。

## How it works

スケジュールは function.json の `schedule` に 6 フィールドの cron 式で書く。ここでは `0 */1 * * * *` = "秒が 0 のとき、毎分" 。

## Learn more

- https://learn.microsoft.com/azure/azure-functions/functions-bindings-timer
