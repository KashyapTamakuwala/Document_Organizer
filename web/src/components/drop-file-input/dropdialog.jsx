import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
// import DialogTitle from '@mui/material/DialogTitle';
import useMediaQuery from '@mui/material/useMediaQuery';
import { useTheme } from '@mui/material/styles';
import DropFileInput from './DropFileInput';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import DriveFolderUploadIcon from '@mui/icons-material/DriveFolderUpload';
import axios from 'axios';

export const ResponsiveDialog = () => {
  const [open, setOpen] = React.useState(false);
  const theme = useTheme();
  const fullScreen = useMediaQuery(theme.breakpoints.down('sm'));
  const [fileList, setFileList] = React.useState([])

  const onFileChange = (files) => {
    console.log(files);
    setFileList(files);
}

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleSave = () => {
    console.log("in handle close");
    var fielData = new FormData();
    fielData.append('Name',fileList[0]['name']);
    fielData.append("type",'File');
    fielData.append('Parent_Folder',"root");
    fielData.append("User_id",'1');
    fielData.append('Files',fileList[0]);
    
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
  };
  const handleClose = () => {
    setOpen(false);
  };

  return (
    <div>
        <ListItemButton
            sx={{
              minHeight: 48,
              
            }}
            onClick={handleClickOpen}
          >
            <ListItemIcon>
              <DriveFolderUploadIcon style={{fontSize:30}}  />
            </ListItemIcon>
            <ListItemText primary="Upload" />
        </ListItemButton>
      {/* <Button variant="outlined" onClick={handleClickOpen}>
        Open responsive dialog
      </Button> */}
      <Dialog
        fullWidth={true}
        fullScreen={fullScreen}
        open={open}
        onClose={handleClose}
        aria-labelledby="responsive-dialog-title"
      >
        <DialogContent>
          <DialogContentText>
                <DropFileInput onFileChange={(files) => onFileChange(files)}/>
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button autoFocus onClick={handleClose}>
                Cancel
          </Button>
          <Button onClick={handleSave} autoFocus>
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default ResponsiveDialog;