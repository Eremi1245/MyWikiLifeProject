import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Icon from '../../images/icon-01.svg';
import EditMenu from '../../components/DropdownEditMenu';


class NoteItem extends Component {
  constructor(props) {
    super(props);
    this.state = {
      initialTitle: props.note.title,
      initialContent: props.note.content,
      title: props.note.title,
      content: props.note.content,
      isEditing: false,
      isSaving: false,
      isDeleting: false,
      isDeleted: false,
    };
  }

  handleEdit = () => {
    const { isEditing } = this.state;
    this.setState({
      isEditing: !isEditing,
      isSaving: false,
    });
  };

  handleChange = (e) => {
    const { name, value } = e.target;
    this.setState({ [name]: value });
  };

  handleSave = () => {
    const { note } = this.props;
    const { title, content } = this.state;
    fetch(`http://localhost:8000/notes/${note.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ title, content }),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Заметка успешно сохранена:', data);
        this.setState({
          initialTitle: data.title,
          initialContent: data.content,
          isEditing: false,
          isSaving: false,
        });
      })
      .catch(error => {
        console.error('Ошибка сохранения заметки:', error);
        this.setState({ isSaving: false });
      });
  };

  handleCancel = () => {
    this.setState(prevState => ({
      title: prevState.initialTitle,
      content: prevState.initialContent,
      isEditing: false,
      isSaving: false,
    }));
  };

  handleDelete = () => {
    this.setState({ isDeleting: true });
  
    const { note, onDelete } = this.props;
  
    if (window.confirm('Вы действительно хотите удалить эту заметку?')) {
      fetch(`http://localhost:8000/notes/${note.id}`, {
        method: 'DELETE',
      })
        .then(response => response.json())
        .then(data => {
          console.log('Заметка успешно удалена:', data);
          this.setState({ isDeleted: true }); // Устанавливаем флаг удаления
        })
        .catch(error => {
          console.error('Ошибка удаления заметки:', error);
          this.setState({ isDeleting: false });
        });
    } else {
      this.setState({ isDeleting: false });
    }
  };

  render() {
    const { note } = this.props;
    const { title, content, isEditing, isSaving, isDeleting, isDeleted  } = this.state;

    const itemClassName = `flex flex-col col-span-full sm:col-span-6 xl:col-span-4 bg-white dark:bg-slate-800 shadow-lg rounded-sm border border-slate-200 dark:border-slate-700 ${
      isDeleted ? 'opacity-50' : ''
    }`;

    return (
      <div className={itemClassName}>
        <div className="px-5 pt-5">
          <header className="flex justify-between items-start mb-2">
            <img src={Icon} width="32" height="32" alt="Icon 01" />
            <EditMenu align="right" className="relative inline-flex">
              <li>
                <button
                  className="font-medium text-sm text-slate-600 dark:text-slate-300 hover:text-slate-800 dark:hover:text-slate-200 flex py-1 px-3"
                  onClick={this.handleEdit}
                >
                  Edit
                </button>
              </li>
              <li>
                <button
                  className="font-medium text-sm text-rose-500 hover:text-rose-600 flex py-1 px-3"
                  onClick={this.handleDelete}
                  disabled={isDeleting}
                >
                  Удалить
                </button>
              </li>
            </EditMenu>
          </header>
          <div className="text-xs font-semibold text-slate-400 dark:text-slate-500 uppercase mb-1">{note.created_at}</div>
          {isEditing ? (
            <input type="text" name="title" value={title} onChange={this.handleChange} />
          ) : (
            <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-2">{title}</h2>
          )}
          <div className="flex items-start">
            {isEditing ? (
              <input type="text" name="content" value={content} onChange={this.handleChange} />
            ) : (
              <div className="text-3xl font-bold text-slate-800 dark:text-slate-100 mr-2">{content}</div>
            )}
            <div className="text-sm font-semibold text-white px-1.5 bg-emerald-500 rounded-full">new</div>
          </div>
          {isEditing && (
            <div className="mt-4">
              <button
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                onClick={this.handleSave}
                disabled={isSaving}
              >
                {isSaving ? 'Сохранение...' : 'Сохранить'}
              </button>
              <button
                className="inline-flex items-center ml-2 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-gray-500 bg-transparent hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                onClick={this.handleCancel}
              >
                Отменить
              </button>
            </div>
          )}
          {isDeleting && (
            <div className="mt-4">
              <p>Вы действительно хотите удалить эту заметку?</p>
              <button
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-500 hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                onClick={this.handleDelete}
                disabled={isDeleting}
              >
                {isDeleting ? 'Удаление...' : 'Подтвердить удаление'}
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }
}

export default NoteItem;
