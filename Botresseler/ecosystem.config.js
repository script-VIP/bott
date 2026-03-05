module.exports = {
  apps: [{
    name: "botresseler",
    script: "app.js",
    cwd: "/root/Botresseler",
    instances: 1,
    exec_mode: "fork",
    autorestart: true,
    watch: false,
    max_memory_restart: "500M",
    error_file: "/root/.pm2/logs/botresseler-error.log",
    out_file: "/root/.pm2/logs/botresseler-out.log",
    log_date_format: "YYYY-MM-DD HH:mm:ss"
  }]
};
