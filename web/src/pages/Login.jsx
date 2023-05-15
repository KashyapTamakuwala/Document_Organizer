import React, { useState} from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Cookies from 'js-cookie';
import { useHistory } from 'react-router';
// import {toast} from 'react-hot-toast';

import axios from 'axios';

const theme = createTheme();


export const Login = () => {

  // eslint-disable-next-line
  const history = useHistory();
 

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const onEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const onPasswordChange = (e) => {
    setPassword(e.target.value);
  };


  const handleSubmit = (event) => {
    event.preventDefault();

    const payload = {
      'email': email,
      'password': password
    }

    axios.post('http://localhost:8000/user/login',payload)
    .then( async (response) => {
      if(response.status !== 200)
      {
        return;
      };
      const accesstoken= response.data.access;
      const payload = {'token':accesstoken}
      axios.post("http://localhost:8000/user/id",payload)
      .then(async (response) =>
      {
        if(response.status !== 200)
        {
          return;
        };
        Cookies.set('ID', response.data, { expires: 1 });
      }).catch((err) => {
        console.log(err)
      })
      Cookies.set('token', accesstoken, { expires: 1 });
      // toast.success("Success"); not working
      
      history.push({pathname:'/homepage',state:{'Current_Folder':'root'}});

    })
    .catch( (err) => {
      // toast.error("Wrong Username or Password")
      console.log(err);
    });

  };

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: "25%",
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar 
          src={require('../assets/user.jpg')}
          sx={{ m: 1, width: 100, height: 100}}>
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              autoComplete="email"
              autoFocus
              value={email}
              onChange={onEmailChange}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              value={password}
              onChange={onPasswordChange}
            />
            <FormControlLabel
              control={<Checkbox value="remember" color="primary" />}
              label="Remember me"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
            <Grid container>
              <Grid item xs>
                <Link href="#" variant="body2">
                  Forgot password?
                </Link>
              </Grid>
              <Grid item>
                <Link href="/register" variant="body2">
                  {"Don't have an account? Sign Up"}
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
        
      </Container>
    </ThemeProvider>
  );
}

export default Login;