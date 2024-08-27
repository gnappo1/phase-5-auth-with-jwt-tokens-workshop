// 📚 Review With Students:
// Request response cycle
//Note: This was build using v5 of react-router-dom
import { Outlet, useNavigate } from 'react-router-dom'
import { createGlobalStyle } from 'styled-components'
import { useEffect, useState } from 'react'
import Header from './components/navigation/Header'
import toast, { Toaster } from "react-hot-toast"
import "./App.css"

function App() {
  const [productions, setProductions] = useState([])
  const [currentUser, setCurrentUser] = useState(null);
  const [production_edit, setProductionEdit] = useState(false)
  const navigate = useNavigate()

  //5.✅ GET Productions
  useEffect(() => {
    fetch("/productions")
    .then(resp => {
      if (resp.ok) { //! 200-299
        resp.json().then(setProductions)
      } else {
        resp.json().then(errorObj => toast.error(errorObj.error))
      }
    })
    .catch(errorObj => toast.error(errorObj.message))
  }, []);
  
  useEffect(() => {
    fetch("/me")
    .then(resp => {
      if (resp.ok) {
        resp.json().then(setCurrentUser)
      } else {
        resp.json().then(errorObj => toast.error(errorObj.error))
      }
    })
      .catch(errorObj => toast.error(errorObj.message))
  }, []);
  // 6.✅ navigate to client/src/components/ProductionForm.js

  const addProduction = (production) => setProductions(productions => [...productions, production])
  const updateProduction = (updated_production) => setProductions(productions => (
    productions.map(production => production.id === updated_production.id ? updated_production : production)
  ))
  const deleteProduction = (deleted_production) => setProductions(productions => (
    productions.filter((production) => production.id !== deleted_production.id)
  ))

  const handleEdit = (production) => {
    setProductionEdit(production)
    navigate(`/productions/${production.id}/edit`)
  }

  const updateUser = (value) => setCurrentUser(value)

  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  return (
    <>
      <GlobalStyle />
      <Header handleEdit={handleEdit} currentUser={currentUser} updateUser={updateUser} />
      <Toaster />
      <Outlet context={{ currentUser, updateUser, addProduction, updateProduction, deleteProduction, productions, production_edit, handleEdit, getCookie }} />
    </>
  )
}

export default App

const GlobalStyle = createGlobalStyle`
    body{
      background-color: black; 
      color:white;
    }
    `
