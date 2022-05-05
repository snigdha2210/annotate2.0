import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom'; //for navigation
import UserIdForm from './UserIdForm'; //User Id Form component
import Header from './Header'; //High level component
import Annotate from './Annotate'; //Component with all main functionalities

const AppRouter = () => (
  <BrowserRouter>
    <div className='container'>
      <Header />
      <Routes>
        <Route element={<UserIdForm />} path='/' exact />
        <Route element={<Annotate />} path='/annotate/:id' />
      </Routes>
    </div>
  </BrowserRouter>
);

export default AppRouter;
