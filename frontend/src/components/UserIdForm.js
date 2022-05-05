import { useState } from 'react';
import './App.css';
import { useNavigate } from 'react-router-dom';

function UserIdForm(props) {
  const navigate = useNavigate();

  //state variable to store user Id from subject
  const [userId, setUserId] = useState('');

  const handleOnChange = (e) => {
    setUserId(e.target.value);
    console.log(e.target.value);
  };

  const handleSubmit = (e) => {
    //prevent reloading of app on submit
    e.preventDefault();

    //navigate to Annotate component
    navigate(`/annotate/${userId}`, { state: userId }); //
  };

  return (
    <div className='App'>
      <form className='form-user-id' onSubmit={handleSubmit}>
        <label>
          Enter User Id:
          <input type='text' name='userId' onChange={handleOnChange} />
        </label>
        <input type='submit' value='Submit' />
      </form>
    </div>
  );
}

export default UserIdForm;
