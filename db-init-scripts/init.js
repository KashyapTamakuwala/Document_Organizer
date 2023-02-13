print('Start #################################################################');

db = db.getSiblingDB('File');
db.createUser({
  user: 'documentorganizeradmin',
  pwd: 'password',
  roles: [{ role: 'readWrite', db: 'File' }],
});
// db.createCollection('Files');



print('END #################################################################');