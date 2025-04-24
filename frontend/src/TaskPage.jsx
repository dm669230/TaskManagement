import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function TaskPage() {
  const [tasks, setTasks] = useState([]);
  const [form, setForm] = useState({ title: '', description: '',task : '', etc: '', due_date: '' });
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  useEffect(() => {
    if (!token) navigate('/login');
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    const user_id = parseJwt(token).id;
    const res = await axios.get(`http://localhost:8000/api/tasks/?user_id=${user_id}`);
    setTasks(res.data);
  };

  const parseJwt = (token) => {
    try {
      return JSON.parse(atob(token.split('.')[1]));
    } catch (e) {
      return null;
    }
  };

  const handleCreateTask = async (e) => {
    e.preventDefault();
    try {
      // const user_id = parseJwt(token).id;
      await axios.post('http://localhost:8000/task_add', { ...form });
      setForm({ title: '', description: '',task : '', etc: '', due_date: '' });
      fetchTasks();
    } catch (err) {
      alert('Task creation failed');
    }
  };

  const handleDelete = async (id) => {
    await axios.delete(`http://localhost:8000/task_delete/`);
    fetchTasks();
  };

  const exportTasks = async () => {
    const user_id = parseJwt(token).id;
    const res = await axios.get(`http://localhost:8000/task_excel`, { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'tasks.xlsx');
    document.body.appendChild(link);
    link.click();
  };

  return (
    <div className="task-page">
      <h2>Your Tasks</h2>

      <form onSubmit={handleCreateTask}>
        <input type="text" placeholder="Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required />
        <input type="text" placeholder="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} required />
        <input type="number" placeholder="Effort (days)" value={form.effort_to_complete} onChange={(e) => setForm({ ...form, effort_to_complete: e.target.value })} required />
        <input type="date" value={form.due_date} onChange={(e) => setForm({ ...form, due_date: e.target.value })} required />
        <button type="submit">Create Task</button>
      </form>

      <button onClick={exportTasks} style={{ marginTop: '20px' }}>Export to Excel</button>

      <ul>
        {tasks.map(task => (
          <li key={task.id}>
            <strong>{task.title}</strong> - {task.description} | Due: {task.due_date}
            <button onClick={() => handleDelete(task.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TaskPage;
