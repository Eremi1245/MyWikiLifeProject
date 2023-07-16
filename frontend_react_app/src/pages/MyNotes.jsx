import React, { useState, useEffect } from 'react';
import Sidebar from '../partials/Sidebar';
import Header from '../partials/Header';
import WelcomeBanner from '../partials/dashboard/WelcomeBanner';
import Banner from '../partials/Banner';
import NoteItem from '../partials/notes/NoteItem';
import Icon from '../images/icon-01.svg';

const MyNotes = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [notes, setNotes] = useState([]);
  const [newNote, setNewNote] = useState({
    title: '',
    created_at: '',
    content: ''
  });

  const createNote = () => {
    fetch('http://localhost:8000/notes/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newNote)
    })
      .then(res => res.json())
      .then(result => {
        // В случае успешного создания заметки обновляем состояние notes
        setNotes([...notes, result]);
        // Сброс состояния newNote
        setNewNote({
          title: '',
          created_at: '',
          content: ''
        });
      })
      .catch(error => {
        // Обработка ошибок при отправке заметки
        console.error('Error creating note:', error);
      });
  };

  const handleSaveNote = () => {
    if (newNote.title && newNote.content) {
      createNote();
    } else {
      console.error('Please enter title and content.');
    }
  };

  useEffect(() => {
    fetch('http://localhost:8000/notes/')
      .then(res => res.json())
      .then(
        result => {
          setIsLoaded(true);
          setNotes(result);
        },
        // Примечание: важно обрабатывать ошибки именно здесь, а не в блоке catch(),
        // чтобы не перехватывать исключения из ошибок в самих компонентах.
        error => {
          setIsLoaded(true);
          setError(error);
        }
      );
  }, []);

  let content = null;

  if (error) {
    content = <div>Ошибка: {error.message}</div>;
  } else if (!isLoaded) {
    content = <div>Загрузка...</div>;
  } else {
    content = (
      <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
        {/* Welcome banner */}
        <WelcomeBanner userName="Alexander" greeting="This is your Notes" description="" />
                {/* Форма создания новой заметки */}
                <div className="mt-4">
          <input
            type="text"
            placeholder="Заголовок"
            value={newNote.title}
            onChange={e => setNewNote({ ...newNote, title: e.target.value })}
          />
          <textarea
            placeholder="Содержимое"
            value={newNote.content}
            onChange={e => setNewNote({ ...newNote, content: e.target.value })}
          />
          <button
            className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded"
            onClick={handleSaveNote}
          >
            Сохранить
          </button>
        </div>
        {/* Cards */}
        <div className="grid grid-cols-12 gap-6">
          {/* Цикл для создания компонентов NoteItem */}
          {notes.map(note => (
            <NoteItem key={note.id} note={note} />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <Sidebar sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

      {/* Content area */}
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
        {/*  Site header */}
        <Header sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

        <main>{content}</main>
        <Banner />
      </div>
    </div>
  );
};

export default MyNotes;
