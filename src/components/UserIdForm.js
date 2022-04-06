import './App.css';

function UserIdForm() {
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

export default UserIdForm;
