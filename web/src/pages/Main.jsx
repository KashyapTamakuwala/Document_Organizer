import React, { useState, useEffect } from 'react';
//import * as React from 'react'
import { styled } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Header from '../components/header';
import FolderCard from '../components/foldercard'
import Grid from '@mui/material/Grid'
import axios from 'axios'

const DrawerHeader = styled('div')(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar,
  }));

export const Main =() => {

    const [dataContent,setDataContent] = useState([]);

    useEffect(() =>
    {
        const userid = 1;
        const url = `http://127.0.0.1:7002/folder/${userid}`;

        axios.get(url)
        .then( async (response) => {
        setDataContent(response.data[0]['FileList']);

         })
        .catch( (err) => {
        // toast.error("Wrong Username or Password")
        console.log(err);
        });

    },[]);

    console.log(typeof(dataContent)) // datacontent is type of string change to array

return (

    <Box bgcolor="" sx={{display:'flex'}}>
        <Header/>
        <Box component='main' sx={{ flexGrow: 1, p: 3 }}>
            <DrawerHeader />
            <CssBaseline/>
           

            <Grid container direction="row" alignItems="center" spacing={{xs: 2}} sx={{paddingLeft:'6%'}}>
                {/* {
                    dataContent.map( () => 
                    {
                        console.log(suceess);
                    }
                    )
                } */}
                <FolderCard prop={{text:'Folder',type:'Folder'}}/>
                <FolderCard prop={{text:'Folder',type:'Folder'}}/>
                <FolderCard prop={{text:'Folder',type:'Folder'}}/>
                <FolderCard prop={{text:'Folder',type:'Folder'}}/>
                <FolderCard prop={{text:'File',type:'File'}}/>
            </Grid>
        </Box >
        
    </Box>
);
}

export default Main;