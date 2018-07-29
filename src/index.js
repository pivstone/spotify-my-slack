if (process.env.NEW_RELIC_ENABLED === 'true') { require('newrelic') }
const assert = require('assert')
const express = require('express')
const path = require('path')
const sleep = require('util').promisify(setTimeout)
const views = require('./views')
const PORT = process.env.PORT || 5000

assert.ok(process.env.DATABASE_URL)
assert.ok(process.env.SET_STATUSES_SLEEP_INTERVAL)

/* express app setup */
const app = express()
app.use('/static', express.static(path.join(__dirname, 'static')))
app.use('/static', express.static(path.join(__dirname, '../node_modules')))
app.use('/vue', express.static(path.join(__dirname, 'vue')))
app.set('views', path.join(__dirname, 'templates'))
app.set('view engine', 'ejs')

/* router setup */
app.get('/', views.root)
app.get('/users', views.users)

/* work loop */
async function setStatuses () {
  console.log('Pretending to set Slack statuses')
  await sleep(process.env.SET_STATUSES_SLEEP_INTERVAL)
  setStatuses()
}
setStatuses()

/* wait for requests */
app.listen(PORT, () => console.log(`Listening on ${PORT}`))
