import React, { useState } from "react";
import axiosInstance from "../../axios";
import { useHistory } from "react-router-dom";
//MaterialUI
import Avatar from "@material-ui/core/Avatar";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";

const useStyles = makeStyles((theme) => ({
    paper: {
        marginTop: theme.spacing(8),
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
    },
    avatar: {
        margin: theme.spacing(1),
        backgroundColor: theme.palette.secondary.main,
    },
    form: {
        width: "100%", // Fix IE 11 issue.
        marginTop: theme.spacing(3),
    },
    submit: {
        margin: theme.spacing(3, 0, 2),
    },
}));

export default function Create() {
    const history = useHistory();
    const initialFormData = Object.freeze({
        title: "",
        excerpt: "",
        content: "",
    });

    const [postData, updateFormData] = useState(initialFormData);
    const [postimage, setPostImage] = useState(null);

    const handleChange = (e) => {
        if (e.target.name === "image") {
            setPostImage({
                image: e.target.files,
            });
            console.log(e.target.files);
        } else {
            updateFormData({
                ...postData,
                [e.target.name]: e.target.value.trim(),
            });
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        let formData = new FormData();
        formData.append("title", postData.title);
        formData.append("author", 1);
        formData.append("excerpt", postData.excerpt);
        formData.append("content", postData.content);
        console.log(postimage.image);
        formData.append("image", postimage.image[0]);
        axiosInstance.post("", formData);
        history.push({
            pathname: "/admin/",
        });
        window.location.reload();
    };

    const classes = useStyles();

    return (
        <Container component="main" maxWidth="xs">
            <CssBaseline />
            <div className={classes.paper}>
                <Avatar className={classes.avatar}></Avatar>
                <Typography component="h1" variant="h5">
                    Create New Post
                </Typography>
                <form className={classes.form} noValidate>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <TextField
                                variant="outlined"
                                required
                                fullWidth
                                id="title"
                                label="Post Title"
                                name="title"
                                autoComplete="title"
                                onChange={handleChange}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                variant="outlined"
                                required
                                fullWidth
                                id="excerpt"
                                label="Post Excerpt"
                                name="excerpt"
                                autoComplete="excerpt"
                                onChange={handleChange}
                                multiline
                                rows={4}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                variant="outlined"
                                required
                                fullWidth
                                id="content"
                                label="content"
                                name="content"
                                autoComplete="content"
                                onChange={handleChange}
                                multiline
                                rows={4}
                            />
                        </Grid>
                        <input
                            accept="image/*"
                            className={classes.input}
                            id="post-image"
                            onChange={handleChange}
                            name="image"
                            type="file"
                        />
                    </Grid>
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        color="primary"
                        className={classes.submit}
                        onClick={handleSubmit}
                    >
                        Create Post
                    </Button>
                </form>
            </div>
        </Container>
    );
}
