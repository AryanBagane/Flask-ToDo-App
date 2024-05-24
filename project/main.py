from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from . import db
from .models import Todo

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    This function renders the index page.
    If the user is authenticated, their name is displayed; otherwise, 'Guest' is displayed.

    Returns:
        render_template: The rendered index.html template with the user's name.
    """
    user_name = current_user.name if current_user.is_authenticated else 'Guest'
    return render_template('index.html', name=user_name)

@main.route('/profile')
@login_required
def profile():
    """
    This function retrieves all the todos of the current user and renders the profile page.

    Returns:
        render_template: The rendered profile.html template with the list of todos.
    """
    todos = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.id.desc()).all()
    return render_template('profile.html', todos=todos)

@main.route('/profile', methods=['POST'])
@main.route('/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def manage_todo(todo_id=None):
    """
    This function handles both GET and POST requests for managing todos.
    If the request method is POST, it creates a new todo or updates an existing one.
    If the request method is GET, it retrieves a specific todo or all todos for the profile page.

    Args:
        todo_id (int, optional): The id of the todo to be managed. Defaults to None.

    Returns:
        redirect: Redirects to the profile page after creating or updating a todo.
        render_template: The rendered profile.html template with the list of todos and a specific todo (if applicable).
    """
    if request.method == 'POST':
        title = request.form.get('title')

        if not title.strip():  # Check if the title is empty or contains only whitespace
            flash('Todo title cannot be empty.')
            return redirect(url_for('main.manage_todo', todo_id=todo_id) if todo_id else url_for('main.profile'))
        
        # Update existing todo if todo_id is provided
        if todo_id:
            todo = Todo.query.get(todo_id)
            if todo and todo.user_id == current_user.id:
                todo.title = title
            else:
                flash('Todo not found or you do not have permission to edit this todo.')
                return redirect(url_for('main.profile'))
        else:
            # Create new todo
            todo = Todo(title=title, user_id=current_user.id, date=datetime.utcnow().date(), created_at=datetime.utcnow())
            db.session.add(todo)
        
        db.session.commit()
        return redirect(url_for('main.profile'))

    # Handle GET request
    todo = None
    if todo_id:
        todo = Todo.query.get(todo_id)
        if todo and todo.user_id!= current_user.id:
            flash('You do not have permission to view this todo.')
            return redirect(url_for('main.profile'))
    
    todos = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.id.desc()).all()
    return render_template('profile.html', todos=todos, todo=todo)

@main.route('/delete/<int:todo_id>', methods=['POST'])
@login_required
def delete_todo(todo_id):
    """
    This function deletes a specific todo.

    Args:
        todo_id (int): The id of the todo to be deleted.

    Returns:
        redirect: Redirects to the profile page after deleting a todo.
    """
    todo = Todo.query.get(todo_id)
    if todo and todo.user_id == current_user.id:
        title = todo.title  # Capture the title before deleting
        db.session.delete(todo)
        db.session.commit()
        flash(f'Todo "{title}" deleted successfully')
    return redirect(url_for('main.profile'))
