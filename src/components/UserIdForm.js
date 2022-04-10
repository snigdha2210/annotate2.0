import { useState } from 'react';
import './App.css';
import { BrowserRouter, useNavigate } from 'react-router-dom';

function UserIdForm(props) {
  const navigate = useNavigate();

  const [userId, setUserId] = useState('');

  const handleOnChange = (e) => {
    setUserId(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // <Navigate to={{ pathname: '/annotate', data: { userId } }} />;

    navigate('/annotate', { state: userId });

    // BrowserRouter.push({
    //   //browserHistory.push should also work here
    //   pathname: '/annotate',
    //   state: { userId: userId },
    // });
  };

  return (
    <div className='App'>
      <form className='form-user-id'>
        <label>
          Enter User Id:
          <input type='text' name='userId' onChange={handleOnChange} />
        </label>
        <input type='submit' value='Submit' onSubmit={handleSubmit} />
      </form>
    </div>
  );
}

export default UserIdForm;
