import * as React from 'react';
// import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
// import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
// import DialogContentText from '@mui/material/DialogContentText';
// import DialogTitle from '@mui/material/DialogTitle';
import CircularProgress from '@mui/material/CircularProgress';


export const LoaderDialog = (Loading) => {
//   const [open, setOpen] = React.useState(true);

//   const handleClickOpen = () => {
//     setOpen(true);
//   };

//   const handleClose = () => {
//     setOpen(false);
//   };
  // console.log(Loading.Loading)
  return (
    <div>
      <Dialog
        open={Loading.Loading}
        // onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
        fullWidth = {true}
        maxWidth = 'sm'
      >
        <DialogContent>
            <CircularProgress sx={{marginLeft:'45%'}}/>
        </DialogContent>
      </Dialog>
    </div>
  );
}

export default LoaderDialog;