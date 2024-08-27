import React, {useState} from 'react'
import styled from 'styled-components'
import { useNavigate, useOutletContext } from 'react-router-dom'
import {object, string, number} from "yup"
import { Formik } from 'formik'
import toast from "react-hot-toast"

// 6.✅ Verify formik and yet have been added to our package.json dependencies 
  // import the useFormik hook or the Formik component from formik
  // import * as yup for yup

let productionSchema = object({
  title: string("title must be of type string").required("title is required").min(1, "titles must contain at least one character"),
  genre: string("genre must be of type string").required("genre is required").oneOf(["Drama", "Musical", "Opera"], "Genre must be one of Musical, Opera or Drama"),
  budget: number("budget must be of type number").positive("budget must be positive").max(1000000, "budget can be 1000000 at max").required("budget must be present"),
  image: string().test("is-url", "image must be in the format jpg, jpeg, or png and start with http or https", (value) => {
    const regexPattern = /^https?:\/\/.*\.(?:png|jpeg|jpg)$/g
    return regexPattern.test(value)
  }),
  director: string("director must be of type string").required("director is required").min(1, "director must contain at least one character"),
  description: string("description must be of type string").required("description is required").min(10, "description has to be at least 10 characters"),
});

const initialValues = {
  title: "",
  genre: "",
  budget: "",
  image: "",
  director: "",
  description: "",
}


function ProductionForm() {
  const { addProduction, getCookie } = useOutletContext()

  const navigate = useNavigate()

  // 7.✅ Use yup to create client side validations
 


  // 9.✅ useFormik hook or <Formik> component


    return (
      <div className='App'>
        <Formik
          initialValues={initialValues}
          validationSchema={productionSchema}
          onSubmit={(formData) => {
            fetch("/productions", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                "X-CSRF-TOKEN": getCookie("csrf_access_token")
              },
              body: JSON.stringify(formData)
            })
            .then(resp => {
              if (resp.ok) {
                resp.json().then(createdProduction => {
                  addProduction(createdProduction)
                  navigate(`/productions/${createdProduction.id}`)
                })
              } else {
                resp.json().then(errorObj => toast.error(errorObj.error))
              }
            })
            .catch(errorObj => toast.error(errorObj.message))
          }}
        >
          {({values, errors, touched, isSubmitting, handleBlur, handleChange, handleSubmit}) => (
            <Form onSubmit={handleSubmit}>
              <label>Title </label>
              <input type='text' name='title'  onChange={handleChange} onBlur={handleBlur} value={values.title} />
              {errors.title && touched.title && <p className='error-message show'>{errors.title}</p>}

              <label> Genre</label>
              <input type='text' name='genre'  onChange={handleChange} onBlur={handleBlur} value={values.genre} />
              {errors.genre && touched.genre && <p className='error-message show'>{errors.genre}</p>}

              <label>Budget</label>
              <input type='number' name='budget'  onChange={handleChange} onBlur={handleBlur} value={values.budget} />
              {errors.budget && touched.budget && <p className='error-message show'>{errors.budget}</p>}

              <label>Image</label>
              <input type='text' name='image'   onChange={handleChange} onBlur={handleBlur} value={values.image} />
              {errors.image && touched.image && <p className='error-message show'>{errors.image}</p>}

              <label>Director</label>
              <input type='text' name='director' onChange={handleChange} onBlur={handleBlur} value={values.director} />
              {errors.director && touched.director && <p className='error-message show'>{errors.director}</p>}

              <label>Description</label>
              <textarea type='text' rows='4' cols='50' name='description'  onChange={handleChange} onBlur={handleBlur} value={values.description} />
              {errors.description && touched.description && <p className='error-message show'>{errors.description}</p>}

              <input type='submit' disabled={isSubmitting}/>
            </Form> 
          )}
        </Formik>
      </div>
    )
  }
  
  export default ProductionForm

  const Form = styled.form`
    display:flex;
    flex-direction:column;
    width: 400px;
    margin:auto;
    font-family:Arial;
    font-size:30px;
    input[type=submit]{
      background-color:#42ddf5;
      color: white;
      height:40px;
      font-family:Arial;
      font-size:30px;
      margin-top:10px;
      margin-bottom:10px;
    }
  `