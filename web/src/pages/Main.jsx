import * as React from 'react';
import { styled } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Header from '../components/header';
import FolderCard from '../components/foldercard'
import Grid from '@mui/material/Grid'
//import DropzoneDialog from '../components/upload';

// const sty = styled('div')(({ theme }) => ({
//     display: 'flex',
//     alignItems: 'center',
//     justifyContent: 'flex-end',
//     padding: theme.spacing(0, 1),
//     // necessary for content to be below app bar
//     ...theme.mixins.toolbar,
//   }));

const DrawerHeader = styled('div')(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar,
  }));

export const Main =() => {

return (

    <Box bgcolor="" sx={{display:'flex'}}>
        <Header/>
        <Box component='main' sx={{ flexGrow: 1, p: 3 }}>
            <DrawerHeader />
            <CssBaseline/>
           

            <Grid container direction="row" alignItems="center" spacing={{xs: 2}} sx={{paddingLeft:'6%'}}>
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