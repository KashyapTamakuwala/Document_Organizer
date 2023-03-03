print('Start #################################################################');

db = db.getSiblingDB('File_manage');
db.createUser({
  user: 'documentorganizeradmin',
  pwd: 'password',
  roles: [{ role: 'readWrite', db: 'File_manage' }],
});
// db.createCollection('Files');



print('END #################################################################');