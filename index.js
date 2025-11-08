const express = require('express');
const app = express();
const PORT = process.env.PORT || 8080;

app.get('/', (req, res) => {
  res.json({ message: 'Hello from sample-app', env: process.env.NODE_ENV || 'dev' });
});

app.listen(PORT, () => {
  console.log(`sample-app listening on ${PORT}`);
});
