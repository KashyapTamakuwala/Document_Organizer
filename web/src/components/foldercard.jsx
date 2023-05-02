import * as React from 'react';
import { styled } from '@mui/material/styles';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { Box, Button, CardActionArea, CardActions } from '@mui/material';
import { ImageConfig } from '../config/ImageConfig'; 


const ExpandMore = styled((props) => {
  const { expand, ...other } = props;
  return <Button {...other} variant='contained' size="small" />;
})(({ theme, expand }) => ({
  marginLeft: 'auto',
}));



export const FolderCard = ({prop}) => {
  //console.log(prop)
  const text = prop.text;
  const type = prop.type;
  const icon = ImageConfig[type];


  return (
    <Box sx={{
      boxShadow:10,
      bgcolor: (theme) => (theme.palette.mode === 'dark' ? '#101010' : '#fff'),
      display:'flex',
      margin:'1%',
      width:300,
    }}>
    <Card sx={{ width:345 }}>
      <CardActionArea>
        <CardMedia
          component="img"
          height="100"
          image={icon}
          alt="Folder Icon"
        />
        <CardContent>
          <Typography gutterBottom variant="h6" component="div" align='center'>
            {text}
          </Typography>
        </CardContent>
      </CardActionArea>
      <CardActions disableSpacing>
        <Button size="small" color="primary" variant='contained'>
          Share
        </Button>
        < ExpandMore>
          Open
        </ExpandMore>
      </CardActions>
    </Card>
    </Box>
  );
}

export default FolderCard;