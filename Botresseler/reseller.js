const fs = require('fs');
const path = require('path');

const resselFilePath = path.join(__dirname, 'ressel.db');

function isUserReseller(userId) {
  if (!fs.existsSync(resselFilePath)) return false;
  const list = fs.readFileSync(resselFilePath, 'utf8').split('\n').map(l => l.trim()).filter(Boolean);
  return list.includes(String(userId));
}

function addReseller(id) {
  const line = `${String(id)}\n`;
  fs.appendFileSync(resselFilePath, line, { encoding: 'utf8' });
}

function removeReseller(id) {
  if (!fs.existsSync(resselFilePath)) return false;
  const content = fs.readFileSync(resselFilePath, 'utf8');
  const lines = content.split('\n').map(l => l.trim()).filter(Boolean);
  const filtered = lines.filter(l => l !== String(id));
  fs.writeFileSync(resselFilePath, filtered.join('\n') + (filtered.length ? '\n' : ''), 'utf8');
  return true;
}

function listResellersSync() {
  if (!fs.existsSync(resselFilePath)) return [];
  const content = fs.readFileSync(resselFilePath, 'utf8');
  return content.split('\n').map(l => l.trim()).filter(Boolean);
}

module.exports = { resselFilePath, isUserReseller, addReseller, removeReseller, listResellersSync };
