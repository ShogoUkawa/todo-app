'use client';

import { useState } from 'react';

import { useTodos } from '../hooks/useTodos';

export function TodoList() {
  const { todos, loading, error, create, complete, remove } = useTodos();
  const [title, setTitle] = useState('');

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: 'red' }}>Error: {error.message}</p>;

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    await create({ title: title.trim() });
    setTitle('');
  };

  return (
    <div>
      <form onSubmit={handleCreate} style={{ marginBottom: '1rem' }}>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="New todo..."
          style={{ padding: '0.5rem', width: '80%' }}
        />
        <button type="submit" style={{ padding: '0.5rem 1rem' }}>
          Add
        </button>
      </form>

      <ul style={{ listStyle: 'none' }}>
        {todos.map((todo) => (
          <li
            key={todo.id}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem',
              padding: '0.5rem 0',
              borderBottom: '1px solid #eee',
            }}
          >
            <span
              style={{
                flex: 1,
                textDecoration: todo.completed ? 'line-through' : 'none',
                color: todo.completed ? '#999' : 'inherit',
              }}
            >
              {todo.title}
            </span>
            {!todo.completed && (
              <button type="button" onClick={() => complete(todo.id)}>
                Done
              </button>
            )}
            <button type="button" onClick={() => remove(todo.id)}>
              Delete
            </button>
          </li>
        ))}
      </ul>

      {todos.length === 0 && <p style={{ color: '#888' }}>No todos yet.</p>}
    </div>
  );
}
