import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import { styled } from '@mui/material/styles';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { Box, Button } from '@mui/material';
import { ImageConfig } from '../config/ImageConfig'; 
import { useHistory } from 'react-router';
import DownloadIcon from '@mui/icons-material/Download';



export const FolderCard = ({prop}) => {
  const theme = useTheme();
  const text = prop.text;
  const type = prop.type;
  const icon = ImageConfig[type];

  const history = useHistory();

  const onOpenFolder = () => {
    console.log("Buuton click")
    history.push({pathname:'/homepage',state:{'Current_Folder':prop.text}})
  }

  const onDownload = () => {
    
  }


  const ExpandMore = styled((props) => {
    const { expand, ...other } = props;
    return <Button {...other} variant='contained' size="small" onClick={onOpenFolder} />;
  })(({ theme, expand }) => ({
    marginLeft: '30%',
  }));

  return (
    <Box sx={{
      boxShadow:10,
      bgcolor: (theme) => (theme.palette.mode === 'dark' ? '#101010' : '#fff'),
      display:'flex',
      margin:'1%',
      width:365,
    }}>

      <Card sx={{ display: 'flex', width:'100%' }}>
          <CardMedia
              component="img"
              sx={{ width: 151 }}
              image={icon}
              alt="Live from space album cover"
          />
          <Box sx={{ display: 'flex',width:'100%', flexDirection: 'column' }}>
              <CardContent sx={{ flex: '1 0 auto' }}>
              <Typography component="div" variant="h5" sx={{marginTop:'10%', marginRight:'2%'}}>
                  {text}
              </Typography>
              </CardContent>
              <Box sx={{ display: 'flex', width:'100%', alignItems: 'center', pl: 1, pb: 1 }}>
              <Button size="small" color="primary" variant='contained' onClick={onDownload} >
                  <DownloadIcon />
              </Button>
              <ExpandMore>Open</ExpandMore>
              </Box>
          </Box>
          
      </Card>
  </Box>
  );
}

export default FolderCard;