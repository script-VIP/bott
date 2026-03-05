module.exports = {
  apps: [{
    name: "botresseler",
    script: "app.js",
    cwd: "/root/bott/Botresseler",
    instances: 1,
    exec_mode: "fork",
    autorestart: true,
    watch: false,
    max_memory_restart: "500M",
    error_file: "/root/bott/Botresseler/logs/error.log",
    out_file: "/root/bott/Botresseler/logs/out.log",
    log_date_format: "YYYY-MM-DD HH:mm:ss"
  }]
};
