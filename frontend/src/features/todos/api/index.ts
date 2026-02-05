import type { CreateTodoPayload, Todo, UpdateTodoPayload } from '../types';

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export async function getTodos(): Promise<Todo[]> {
  const res = await fetch(`${API_URL}/todos`);
  if (!res.ok) throw new Error('Failed to fetch todos');
  return res.json();
}

export async function createTodo(payload: CreateTodoPayload): Promise<Todo> {
  const res = await fetch(`${API_URL}/todos`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Failed to create todo');
  return res.json();
}

export async function updateTodo(
  id: string,
  payload: UpdateTodoPayload,
): Promise<Todo> {
  const res = await fetch(`${API_URL}/todos/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Failed to update todo');
  return res.json();
}

export async function completeTodo(id: string): Promise<Todo> {
  const res = await fetch(`${API_URL}/todos/${id}/complete`, {
    method: 'PATCH',
  });
  if (!res.ok) throw new Error('Failed to complete todo');
  return res.json();
}

export async function deleteTodo(id: string): Promise<void> {
  const res = await fetch(`${API_URL}/todos/${id}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error('Failed to delete todo');
}
