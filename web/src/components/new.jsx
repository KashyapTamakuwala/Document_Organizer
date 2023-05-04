import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import { Button } from '@mui/material';
// import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
// import SkipPreviousIcon from '@mui/icons-material/SkipPrevious';
// import PlayArrowIcon from '@mui/icons-material/PlayArrow';
// import SkipNextIcon from '@mui/icons-material/SkipNext';
import { ImageConfig } from '../config/ImageConfig'; 
import { styled } from '@mui/material/styles';
import DownloadIcon from '@mui/icons-material/Download';
import { useHistory } from 'react-router';


export const Temp = ({prop}) => {
  const theme = useTheme();
  const type = 'pdf' 
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
    return <Button {...other} variant='contained' size="small" onClick={onOpenFolder}/>;
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

        <Card sx={{ display: 'flex', width:'400' }}>
            <CardMedia
                component="img"
                sx={{ width: 151 }}
                image={icon}
                alt="Live from space album cover"
            />
            <Box sx={{ display: 'flex',width:'100%', flexDirection: 'column' }}>
                <CardContent sx={{ flex: '1 0 auto' }}>
                <Typography component="div" variant="h5" sx={{marginTop:'10%'}}>
                    Live From Space
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

export default Temp;