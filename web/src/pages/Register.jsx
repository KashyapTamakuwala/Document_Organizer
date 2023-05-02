
import React, { useState, useEffect } from 'react';
// import { useHistory } from 'react-router';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { validate as validateEmail } from 'email-validator';
import { useHistory } from 'react-router';

import axios from 'axios';

const theme = createTheme();

export const Register = () => {

  // eslint-disable-next-line
  const history = useHistory();

  const [email, setEmail] = useState('');
  const [emailIsVisited, setEmailIsVisited] = useState(false);
  const [emailHasError, setEmailHasError] = useState(false);
  const [emailErrorText, setEmailErrorText] = useState('');
  const emailShouldShowError = !emailHasError && emailIsVisited;

  // eslint-disable-next-line no-unused-vars

  const [password, setPassword] = useState('');
  const [passwordIsVisited, setPasswordIsVisited] = useState(false);
  const [passwordHasError, setPasswordHasError] = useState(false);
  const [passwordErrorText, setPasswordErrorText] = useState('');
  const passwordShouldShowError = !passwordHasError && passwordIsVisited;
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\w\W]{8,}$/;


  const [firstName,setFirstName] = useState('')
  const [lastName,setLastName] = useState('')

  const onFirstNameChange = (e) => {
    setFirstName(e.target.value)
  };

  const onLastNameChange = (e) => {
    setLastName(e.target.value)
  };


  const onEmailChange = (e) => {
    setEmail(e.target.value);
    setEmailHasError(validateEmail(e.target.value));
  };

  const onPasswordChange = (e) => {
    setPassword(e.target.value);
    setPasswordHasError(passwordRegex.test(e.target.value));
  };


  useEffect(() => {
    if (passwordShouldShowError) {
      setPasswordErrorText('Please enter a valid password!');
    } else {
      setPasswordErrorText('');
    }
  }, [passwordShouldShowError]);

  useEffect(() => {
    if (emailShouldShowError) {
      setEmailErrorText('Please enter valid email address!');
    } else {
      setEmailErrorText('');
    }
  }, [emailShouldShowError]);



  
  const handleSubmit = (event) => {
    event.preventDefault();
    if (emailShouldShowError || passwordShouldShowError){
      return;
    }

    console.log("Making register request");
    
    const payload = new FormData();
    payload.append( 'email', email);
    payload.append('first_name', firstName);
    payload.append('last_name', lastName);
    payload.append('password', password);
    payload.append('Confirm_Password',password);


    axios.post('http://127.0.0.1:7001/user/register',payload)
    .then( async (response) => {
      if(response.status !== 201){
        return;
      };
      console.log(response);
      history.push('/');
    })
    .catch( (err) =>{ 
      console.log(err);
    })
    
  };

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: '25%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar src={require('../assets/user.jpg')}
          sx={{ m: 1, width: 100, height: 100}}>
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign up
          </Typography>
          <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  autoComplete="given-name"
                  name="firstName"
                  required
                  fullWidth
                  id="firstName"
                  label="First Name"
                  autoFocus
                  value = {firstName}
                  onChange = {onFirstNameChange}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  required
                  fullWidth
                  id="lastName"
                  label="Last Name"
                  name="lastName"
                  autoComplete="family-name"
                  value = {lastName}
                  onChange = {onLastNameChange} 
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  id="email"
                  label="Email Address"
                  name="email"
                  autoComplete="email"
                  value = {email}
                  onChange = {onEmailChange}
                  error = {emailShouldShowError}
                  helperText = {emailErrorText}
                  onBlur = {() => setEmailIsVisited(true)}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  name="password"
                  label="Password"
                  type="password"
                  id="password"
                  autoComplete="new-password"
                  value = {password}
                  onChange = {onPasswordChange}
                  error = {passwordShouldShowError}
                  helperText = {passwordErrorText}
                  onBlur = {() => setPasswordIsVisited(true)}
                />
              </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign Up
            </Button>
            <Grid container justifyContent="flex-end">
              <Grid item>
                <Link href="/" variant="body2">
                  Already have an account? Sign in
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default Register;