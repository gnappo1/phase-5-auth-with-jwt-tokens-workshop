import { useState, useEffect } from "react";
import { object, string } from "yup";
import { useFormik, Formik } from "formik";
import styled from "styled-components"
import toast from "react-hot-toast"
import { useOutletContext, useNavigate } from "react-router-dom";

const signupSchema = object({
  username: 
    string("username has to be a string")
    .max(25, "username must be 25 characters max")
    .required("username is required"),
  email: 
    string("email has to be a string")
    .email("email must be valid")
    .max(80, "email must be 80 characters max")
    .required("email is required"),
  password_hash: 
    string("password has to be a string")
    .min(8, "password has to be at least 8 characters long")
    .max(25, "password must be 25 characters long max")
    .required("password is required"),
});

const signinSchema = object({
  email: 
    string("email has to be a string")
    .email("email must be valid")
    .max(80, "email must be 80 characters max")
    .required("email is required"),
  password_hash: 
    string("password has to be a string")
    .min(8, "password has to be at least 8 characters long")
    .max(25, "password must be 25 characters long max")
    .required("password is required"),
});

const initialValues = {
    username: "",
    email: "",
    password_hash: "",
}

const Registration = () => {
    const [isLogin, setIsLogin] = useState(true);
    const { updateUser, currentUser } = useOutletContext();

    const navigate = useNavigate()

    useEffect(() => {
      if (currentUser) {
        navigate("/");
      }
    }, [currentUser, navigate]);

    return (
      <div>
        <h2>Please Log in or Sign Up</h2>
        <h3>{isLogin ? "Not a Member?" : "Already a member?"}</h3>
        <button onClick={() => setIsLogin((current) => !current)}>
          {isLogin ? "Register Now!" : "Login!"}
        </button>
        <Formik
          validationSchema={isLogin ? signinSchema : signupSchema}
          initialValues={initialValues}
          onSubmit={(formData) => {
            const finalUrl = isLogin ? "/signin" : "/signup"
            fetch(finalUrl, {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(formData),
            })
              .then((resp) => {
                if (resp.ok) {
                  resp.json().then((user) => {
                    updateUser(user);
                    navigate("/");
                  });
                } else {
                  resp.json().then((errorObj) => toast.error(errorObj.error));
                }
              })
              .catch((errorObj) => toast.error(errorObj.message));
          }}
        >
          {({
            values,
            errors,
            touched,
            isSubmitting,
            handleChange,
            handleSubmit,
            handleBlur,
          }) => (
            <Form onSubmit={handleSubmit}>
              {!isLogin && (
                <>
                  <label htmlFor="username">Username</label>
                  <input
                    type="text"
                    name="username"
                    onChange={handleChange}
                    onBlur={handleBlur}
                    value={values.username}
                  />
                  {errors.username && touched.username && (
                    <p className="error-message show">{errors.username}</p>
                  )}
                </>
              )}
              <label htmlFor="email">Email</label>
              <input
                type="email"
                name="email"
                onChange={handleChange}
                onBlur={handleBlur}
                value={values.email}
              />
              {errors.email && touched.email && (
                <p className="error-message show">{errors.email}</p>
              )}
              <label htmlFor="password_hash">Password</label>
              <input
                type="password"
                name="password_hash"
                onChange={handleChange}
                onBlur={handleBlur}
                value={values.password_hash}
              />
              {errors.password_hash && touched.password_hash && (
                <p className="error-message show">{errors.password_hash}</p>
              )}

              <input
                type="submit"
                value={isLogin ? "Login!" : "Create Account!"}
                disabled={isSubmitting}
              />
            </Form>
          )}
        </Formik>
      </div>
    );
};

export default Registration;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  width: 400px;
  margin: auto;
  font-family: Arial;
  font-size: 30px;
  input[type="submit"] {
    background-color: #42ddf5;
    color: white;
    height: 40px;
    font-family: Arial;
    font-size: 30px;
    margin-top: 10px;
    margin-bottom: 10px;
  }
`;