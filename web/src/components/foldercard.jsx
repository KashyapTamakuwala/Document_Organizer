import * as React from 'react';
import { styled } from '@mui/material/styles';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { Box } from '@mui/material';
import { ImageConfig } from '../config/ImageConfig'; 
import { useHistory } from 'react-router';
import DownloadIcon from '@mui/icons-material/Download';
import IconButton from '@mui/material/IconButton';
import OpenInBrowserIcon from '@mui/icons-material/OpenInBrowser';
import DeleteForeverIcon from '@mui/icons-material/DeleteForever';
import Cookies from 'js-cookie';
import axios from 'axios';
import LoaderDialog from './loader';




export const FolderCard = ({prop}) => {

  const text = prop.text
  const type = prop.type
  // const path = prop.path
  const parent = prop.folder
  // console.log(parent)
  // console.log(path)
  const ext = ["pdf", "png", "jpeg", "css",'jpg','Folder'];
  const icon = ext.includes(type)? ImageConfig[type]:ImageConfig['default'];
  const [isLoading,setIsLoading] = React.useState(false)

  const history = useHistory();



  const onOpenFolder = () => {
    // console.log("Buuton click")
    const userID = Cookies.get("ID")
    if (type === 'Folder'){
      history.push({pathname:'/homepage',state:{'Current_Folder':prop.text}})
    }
    else{
      const url = `http://localhost:8000/uploader/stream/${userID}?name=${text}`
      window.open(url, "_blank")
    }
  }

  const onDownload = () => {
    const userID = Cookies.get("ID");
    if (type==='Folder'){
     
    const url = `http://localhost:8000/file/${userID}`;
    const param = {'fol':text};
    axios.get(url,{params: param})
    .then( async (response) => {
      var data = response.data[0]['FileList']
      var name = ""
      for(let i=0;i<data.length;i++){
        if (data[i]['Family'] !== 'Folder'){
            name = name+data[i]['Name']+","
        }
      }
      name = name.slice(0,-1)
      const durl = `http://localhost:8000/uploader/download/${userID}/?name=${name}`;
      window.open(durl, "_blank")
     })
  }

    else{
      const durl = `http://localhost:8000/uploader/download/${userID}/?name=${text}`;
      window.open(durl, "_blank")
    }
    
  }

  const onDelete = () => {
    const userID = Cookies.get("ID");
    const url = ` http://localhost:8000/file/delete/${userID}`;
    const payload = new FormData();
    payload.append( 'name', parent);
    payload.append('fname', text);
    setIsLoading(true)
    axios.post(url,payload).then((response) => {
      // console.log(response)
      // console.log(payload)
      // console.log(parent,text)
      setIsLoading(false)
      window.location.reload()
    }).catch((err)=> {
      console.log(err)
    })
  }


  const ExpandMore = styled((props) => {
    const { expand, ...other } = props;
    return <IconButton {...other} variant='contained' size="small" onClick={onDelete} />;
  })(({ theme, expand }) => ({
    marginLeft: '23%',
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
          <Box sx={{ display: 'flex', width:'100%', flexDirection: 'column' }}>
              <CardContent sx={{ flex: '1 0 auto' }}>
              <Typography  component="div" variant="h5" sx={{marginTop:'10%', marginRight:'2%'}}>
                  {text}
              </Typography>
              </CardContent>
              <Box sx={{ display: 'flex', width:'100%', alignItems: 'center', pl: 1, pb: 1 }}>
              {/* <Button size="small" color="primary" variant='contained' onClick={onDownload} >
                  <DownloadIcon />
              </Button>
              <ExpandMore>Open</ExpandMore> */}

              <IconButton size='medium' aria-label="previous" onClick={onDownload} sx={{ marginLeft: '0%'}}>
                  <DownloadIcon color='primary'/>
              </IconButton>
              
              <IconButton onClick={onOpenFolder} size='medium' aria-label="next" sx={{ marginLeft: '19%'}}>
                  <OpenInBrowserIcon color='primary'/>
              </IconButton>
              
              <ExpandMore> 
                <DeleteForeverIcon  color='error'/>
              </ExpandMore>
              
              <LoaderDialog Loading={isLoading}/>
              
              </Box>
          </Box>
          
      </Card>
  </Box>
  );
}

export default FolderCard;