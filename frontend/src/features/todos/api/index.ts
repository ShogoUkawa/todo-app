import { supabase } from '@/lib/supabase';
import type { CreateTodoPayload, Todo, UpdateTodoPayload } from '../types';

export async function getTodos(): Promise<Todo[]> {
  const { data, error } = await supabase
    .from('todos')
    .select('*')
    .order('created_at', { ascending: false });

  if (error) throw new Error(`Failed to fetch todos: ${error.message}`);
  return data ?? [];
}

export async function createTodo(payload: CreateTodoPayload): Promise<Todo> {
  const { data, error } = await supabase
    .from('todos')
    .insert([payload])
    .select()
    .single();

  if (error) throw new Error(`Failed to create todo: ${error.message}`);
  return data;
}

export async function updateTodo(
  id: string,
  payload: UpdateTodoPayload,
): Promise<Todo> {
  const { data, error } = await supabase
    .from('todos')
    .update(payload)
    .eq('id', id)
    .select()
    .single();

  if (error) throw new Error(`Failed to update todo: ${error.message}`);
  return data;
}

export async function completeTodo(id: string): Promise<Todo> {
  const { data, error } = await supabase
    .from('todos')
    .update({ completed: true })
    .eq('id', id)
    .select()
    .single();

  if (error) throw new Error(`Failed to complete todo: ${error.message}`);
  return data;
}

export async function deleteTodo(id: string): Promise<void> {
  const { error } = await supabase.from('todos').delete().eq('id', id);

  if (error) throw new Error(`Failed to delete todo: ${error.message}`);
}
