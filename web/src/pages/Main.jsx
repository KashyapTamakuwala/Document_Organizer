import React, { useState, useEffect } from 'react';
//import * as React from 'react'
import { styled } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Header from '../components/header';
import FolderCard from '../components/foldercard'
import Grid from '@mui/material/Grid'
import axios from 'axios'
import { useLocation } from "react-router-dom";
import Cookies from 'js-cookie';
import CreateFolder from '../components/createdialog';
// import CircularProgress from '@mui/material/CircularProgress';


const DrawerHeader = styled('div')(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar,
  }));

export const Main = () => {
    const location = useLocation();
    
    const [dataContent,setDataContent] = useState([]);
    const [searchQuerry,setSerachQuerry] = useState("");
    const [isParent,setIsParent] = useState(false)
    const [parent,setParent] = useState("");

    const folder = location.state.Current_Folder;
    const category = location.state.cat === undefined ? 'None' : location.state.cat;
    
    
    useEffect(()=>{
        const userId =  Cookies.get('ID')
        if (userId === -1){
          window.location.reload()
        }
        const url = `http://localhost:8000/file/${userId}`;
        const param = {'fol':folder,'cat':category};
        axios.get(url,{params: param})
        .then( async (response) => {
            console.log(response)
            const catArray = ['Book','Resume','Publication','Legal','Code','News']
            if (catArray.includes(category)){
                setDataContent(response.data)
                setIsParent(true)
            }
            else {
                if(response.data.length > 0){
                  setDataContent(response.data[0]['FileList']);
                  setParent(response.data[0]['Folder_Name']);
              }
              else{
                setDataContent([]);
                setParent("root");
              }
              
            }
        })
        .catch( (err) => {
        // toast.error("Wrong Username or Password")
        console.log(err);
        window.location.reload()
        });
    },[folder,category]);


    dataContent.sort((a, b) => {
        if (a.Family < b.Family) {
          return -1;
        } else if (a.Family > b.Family) {
          return 1;
        } else {
          if (a.Name < b.Name) {
            return -1;
          } else if (a.Name > b.Name) {
            return 1;
          } else {
            return 0;
          }
        }
      });

    const filteredItem = dataContent.filter((content) => content.Name.toLowerCase().includes(searchQuerry.toLowerCase()) )


return (

    <Box bgcolor="" sx={{display:'flex'}}>
        <Header searchQuerry={searchQuerry} setSerachQuerry={setSerachQuerry}/>
        <Box component='main' sx={{ flexGrow: 1, p: 3 }}>
            <DrawerHeader />
            <CssBaseline/>
            

            <Grid container direction="row" alignItems="center" spacing={{xs: 2}} sx={{paddingLeft:'6%'}}>
                {
                   
                    filteredItem.map( (content) => 
                    {
                        var pf = "";

                        if (isParent){
                          // console.log("is true",pf)
                          pf = content.Parent_Folder
                        }
                        else{
                        // console.log("is false",pf)
                         pf = parent;

                        }
                       
                        if(content.Family === 'File'){
                          const temp = content.Name.split(".");
                          const t = temp[temp.length - 1];
                          return <FolderCard prop={{text:content.Name,type:t,path:content.Path,folder:pf}}/>
                        }
                        else {
                          return <FolderCard prop={{text:content.Name,type:'Folder',path:content.Path,folder:pf}}/>
                        }
                        
                    }
                    )
                }
               
                {/* <FolderCard prop={{text:'Folder',type:'Folder'}}/> */}
                {/* <FolderCard prop={{text:'Folder',type:'Folder'}}/>
                <FolderCard prop={{text:'Folder',type:'Folder'}}/>
                <FolderCard prop={{text:'File',type:'File'}}/> */}
            </Grid>
        </Box >
        {/* <Fab variant="extended" onClick={} color="primary" aria-label="add" sx={{position:'absolute','bottom':16,right:16}}>
          <AddIcon sx={{ mr: 1 }} />
          Create Folder
        </Fab> */}
        <CreateFolder/>
        
    </Box>
);
}

export default Main;