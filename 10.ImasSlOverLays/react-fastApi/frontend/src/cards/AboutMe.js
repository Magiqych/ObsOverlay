import * as React from "react";
import { styled } from "@mui/material/styles";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardMedia from "@mui/material/CardMedia";
import CardContent from "@mui/material/CardContent";
import Avatar from "@mui/material/Avatar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import { red } from "@mui/material/colors";
import Stack from "@mui/material/Stack";

const ExpandMore = styled((props) => {
  const { expand, ...other } = props;
  return <IconButton {...other} />;
})(({ theme }) => ({
  marginLeft: "auto",
  transition: theme.transitions.create("transform", {
    duration: theme.transitions.duration.shortest,
  }),
  variants: [
    {
      props: ({ expand }) => !expand,
      style: {
        transform: "rotate(0deg)",
      },
    },
    {
      props: ({ expand }) => !!expand,
      style: {
        transform: "rotate(180deg)",
      },
    },
  ],
}));

export default function AboutMe() {
  return (
    <Card>
      <Stack direction="row" spacing={2}>
        <CardHeader
          avatar={
            <Avatar alt="Remy Sharp" src="Assets/Magiqych/Magiqych.jpg" />
          }
          title="About Me"
          subheader="youtube.com/@magiqy_ch"
        />
        <div>
          <image src="Assets/Magiqych/Magiqych.jpg" alt="Remy Sharp" />
          <Typography variant="h5" component="h2">
            transient
          </Typography>
        </div>
      </Stack>

      <CardContent>
        <Typography
          variant="h6"
          component="h2"
          sx={{ color: "text.secondary" }}
        >
          I share my life and hobbies, from gaming, manga, and anime to fishing.{" "}
          <br />
          I just want to connect with people from all over the world through
          YouTube.
          <br />
          I don’t have any specific goals —my goal is to have no goals. Life is
          unpredictable, and so is this channel. <br />
          everything is transient, and that’s the theme of my life.
        </Typography>
      </CardContent>
    </Card>
  );
}
