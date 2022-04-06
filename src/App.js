import './App.css';

function App() {
  return (
    <div className='App'>
      <form className='form-user-id'>
        <label>
          Enter User Id:
          <input type='text' name='userId' />
        </label>
        <input type='submit' value='Submit' />
      </form>
    </div>
  );
}

export default App;
