'use client';

import { useCallback, useEffect, useState } from 'react';
import * as api from '../api';
import type { CreateTodoPayload, Todo } from '../types';

export function useTodos() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchTodos = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getTodos();
      setTodos(data);
    } catch (e) {
      setError(e instanceof Error ? e : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTodos();
  }, [fetchTodos]);

  const create = async (payload: CreateTodoPayload) => {
    const todo = await api.createTodo(payload);
    setTodos((prev) => [...prev, todo]);
  };

  const complete = async (id: string) => {
    const updated = await api.completeTodo(id);
    setTodos((prev) => prev.map((t) => (t.id === id ? updated : t)));
  };

  const remove = async (id: string) => {
    await api.deleteTodo(id);
    setTodos((prev) => prev.filter((t) => t.id !== id));
  };

  return {
    todos,
    loading,
    error,
    create,
    complete,
    remove,
    refetch: fetchTodos,
  };
}
