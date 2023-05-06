import * as React from 'react';
import { makeStyles } from "@material-ui/core/styles";
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Fab from '@mui/material/Fab';
import AddIcon from '@mui/icons-material/Add';
import Paper from '@mui/material/Paper';
import Draggable from 'react-draggable';
import axios from 'axios';
import { useLocation } from "react-router-dom";
import { getCookie } from 'react-use-cookie';

const useStyles = makeStyles((theme) => ({
    fab: {
      position: "fixed",
      bottom: theme.spacing(2),
      right: theme.spacing(2),
    },
  }));


const PaperComponent = (props) => {
    return (
      <Draggable
        handle="#draggable-dialog-title"
        cancel={'[class*="MuiDialogContent-root"]'}
      >
        <Paper {...props} />
      </Draggable>
    );
  }

export  const CreateFolder = () => {
  const classes = useStyles();
  const [open, setOpen] = React.useState(false);
  const [text , setText] = React.useState("");

  const [bottomOffset, setBottomOffset] = React.useState(0);

  React.useEffect(() => {
    function handleScroll() {
      setBottomOffset(window.pageYOffset);
    }

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);



  
  const location = useLocation();


  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const onTextChange = (e) => {
    setText(e.target.value);
  };

  const handleCreate = () =>{
    const userId = getCookie('ID');
    var fielData = new FormData();
    fielData.append('Name',text);
    fielData.append("type",'Folder');
    fielData.append('Parent_Folder',location.state.Current_Folder);
    fielData.append("User_id",userId);
    // fielData.append('Files',fileList[0]);
    
    axios.post("http://127.0.0.1:7002/folder/",fielData)
    .then( async (response) => {
      console.log(response);
      if(response.status !== 201){
        return;
      };
      console.log(response);
    })
    .catch( (err) =>{ 
      console.log(err);
    })
    setOpen(false);
    window.location.reload(); 

  }

  return (
    <div>
      <Fab variant="extended" onClick={handleClickOpen} color="primary" aria-label="add" className={classes.fab} sx={{ bottom: 20 + bottomOffset + "px" }}>
          <AddIcon sx={{ mr: 1 }} />
          Create Folder
        </Fab>
      <Dialog open={open} 
        onClose={handleClose} 
        sx = {{width:'30%',margin:'auto'}}
        fullWidth = {true}
        PaperComponent={PaperComponent}
        aria-labelledby="draggable-dialog-title">
        <DialogTitle>Create Folder</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            id="name"
            label="Folder Name"
            type="text"
            fullWidth
            variant="standard"
            value={text}
            onChange={onTextChange}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleCreate}>Create</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default CreateFolder;