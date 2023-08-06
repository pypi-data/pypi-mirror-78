# -*- mode: conf; -*-

# backup everything of importance at ${pretty_time}
${'' if env.machine_is_live else '# '}${cron_time} * * *  root  /usr/local/bin/backup-everything
