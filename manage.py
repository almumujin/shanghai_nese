from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app import app
from exts import db
from models import User
# from main import app, db, User, Post, Tag, Comment

# 使用migrate绑定app和db
migrate = Migrate(app, db)
# 添加迁移脚本的命令到manager中
manager = Manager(app)
# manager.add_command("server", Server())
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User#,
        # Post=Post,
        # Tag=Tag,
        # Comment=Comment
    )

if __name__ == "__main__":
    manager.run()
