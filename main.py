from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("KEY").encode("utf-8")
Bootstrap5(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL") + "?timeout=20"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class ListData(db.Model):
    __tablename__ = "list_data"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    desc: Mapped[str] = mapped_column(String(250))
    date: Mapped[str] = mapped_column(String(250))
    tasks: Mapped[list["TasksData"]] = relationship(back_populates="parent_list")


class TasksData(db.Model):
    __tablename__ = "task_data"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250))
    pending: Mapped[int] = mapped_column(Integer)
    starred: Mapped[int] = mapped_column(Integer)
    color: Mapped[str] = mapped_column(String(250))
    list_id: Mapped[int] = mapped_column(ForeignKey("list_data.id"))
    parent_list: Mapped["ListData"] = relationship(back_populates="tasks")


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    lists = db.session.execute(db.select(ListData)).scalars().all()
    return render_template("index.html", all_lists=lists)


# ====================== CREATE NEW LIST ======================
@app.route("/add_list", methods=["POST"])
def add_list():
    list_name = request.form.get("list_name")

    if not list_name:
        flash("List name cannot be empty!", "danger")
        return redirect(url_for('home'))

    new_list = ListData(
        name=list_name,
        desc="No description yet.",
        date=datetime.now().strftime("%b %d, %Y"),
    )

    db.session.add(new_list)
    db.session.commit()
    # Redirect to the newly created list
    return redirect(url_for('show_list', list_id=new_list.id))


# ====================== ADD TASK ======================
@app.route("/add_task/<int:list_id>", methods=["POST"])
def add_task(list_id):
    task_name = request.form.get("task_name")

    if task_name:
        new_task = TasksData(
            name=task_name,
            date="",
            pending=1,
            starred=0,
            color="#0d6efd",
            list_id=list_id
        )
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully!", "success")
    else:
        flash("Task name cannot be empty.", "danger")

    return redirect(url_for('show_list', list_id=list_id))


# ====================== EDIT LIST ======================
@app.route("/edit_list/<int:list_id>", methods=["POST"])
def edit_list(list_id):
    list_to_edit = db.get_or_404(ListData, list_id)

    list_to_edit.name = request.form.get("name")
    list_to_edit.desc = request.form.get("desc")

    db.session.commit()
    flash("List updated successfully!", "success")

    return redirect(url_for('show_list', list_id=list_id))

# ====================== DELETE TASK ======================
@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = db.get_or_404(TasksData, task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "success")
    return jsonify({'success': True})


# ====================== BUTTONS ======================
@app.route('/toggle_star/<int:task_id>', methods=['POST'])
def toggle_star(task_id):
    task = db.get_or_404(TasksData, task_id)
    task.starred = 1 if task.starred == 0 else 0
    db.session.commit()
    return jsonify({'success': True})

@app.route('/set_color/<int:task_id>', methods=['POST'])
def set_color(task_id):
    task = db.get_or_404(TasksData, task_id)
    data = request.get_json()
    task.color = data.get('color', '#000000')
    db.session.commit()
    return jsonify({'success': True})

@app.route('/set_due_date/<int:task_id>', methods=['POST'])
def set_due_date(task_id):
    task = db.get_or_404(TasksData, task_id)
    data = request.get_json()
    task.date = data.get('date', '')
    db.session.commit()
    return jsonify({'success': True})

@app.route('/toggle_pending/<int:task_id>', methods=['POST'])
def toggle_pending(task_id):
    task = db.get_or_404(TasksData, task_id)
    task.pending = 1 if task.pending == 0 else 0
    db.session.commit()
    return jsonify({'success': True})



# ====================== SHOW LIST ======================
@app.route("/show_list/<int:list_id>")
def show_list(list_id):
    selected_list = db.get_or_404(ListData, list_id)
    return render_template("show_list.html", current_list=selected_list)


if __name__ == "__main__":
    app.run(debug=True, port=5003)