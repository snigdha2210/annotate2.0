import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import UserIdForm from './UserIdForm';
import Header from './Header';
import Annotate from './Annotate';

const AppRouter = () => (
  <BrowserRouter>
    <div className='container'>
      <Header />
      <Routes>
        <Route element={<UserIdForm />} path='/' exact />
        <Route element={<Annotate />} path='/annotate' exact />
      </Routes>
    </div>
  </BrowserRouter>
);

export default AppRouter;
