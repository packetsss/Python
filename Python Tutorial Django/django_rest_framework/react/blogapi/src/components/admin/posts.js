import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";
import Link from "@material-ui/core/Link";
import Paper from "@material-ui/core/Paper";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import DeleteForeverIcon from "@material-ui/icons/DeleteForever";
import EditIcon from "@material-ui/icons/Edit";
import Button from "@material-ui/core/Button";

const useStyles = makeStyles((theme) => ({
    cardMedia: {
        paddingTop: "56.25%", // 16:9
    },
    link: {
        margin: theme.spacing(1, 1.5),
    },
    cardHeader: {
        backgroundColor:
            theme.palette.type === "light"
                ? theme.palette.grey[200]
                : theme.palette.grey[700],
    },
    postTitle: {
        fontSize: "16px",
        textAlign: "left",
    },
    postText: {
        display: "flex",
        justifyContent: "left",
        alignItems: "baseline",

        fontSize: "12px",
        textAlign: "left",
        marginBottom: theme.spacing(2),
    },
}));

const Posts = (props) => {
    const { posts } = props;
    const classes = useStyles();
    if (!posts || posts.length === 0)
        return <p>Can not find any posts, sorry</p>;
    return (
        <React.Fragment>
            <Container maxWidth="md" component="main">
                <Paper className={classes.root}>
                    <TableContainer className={classes.container}>
                        <Table stickyHeader aria-label="sticky table">
                            <TableHead>
                                <TableRow>
                                    <TableCell>Id</TableCell>
                                    <TableCell align="left">Category</TableCell>
                                    <TableCell align="left">Title</TableCell>
                                    <TableCell align="left">Action</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {posts.map((post, i) => {
                                    return (
                                        <TableRow key={(i + 1) * Math.random()}>
                                            <TableCell
                                                key={(i + 1) * Math.random()}
                                                component="th"
                                                scope="row"
                                            >
                                                {post.id}
                                            </TableCell>
                                            <TableCell key={(i + 1) * Math.random()} align="left">
                                                {post.category}
                                            </TableCell>

                                            <TableCell key={(i + 1) * Math.random()} align="left">
                                                <Link
                                                    key={(i + 1) * Math.random()}
                                                    color="textPrimary"
                                                    href={"/post/" + post.slug}
                                                    className={classes.link}
                                                >
                                                    {post.title}
                                                </Link>
                                            </TableCell>

                                            <TableCell key={(i + 1) * Math.random()} align="left">
                                                <Link
                                                    key={(i + 1) * Math.random()}
                                                    color="textPrimary"
                                                    href={
                                                        "/admin/edit/" +
                                                        post.slug
                                                    }
                                                    className={classes.link}
                                                >
                                                    <EditIcon key={(i + 1) * Math.random()}></EditIcon>
                                                </Link>
                                                <Link
                                                    key={(i + 1) * Math.random()}
                                                    color="textPrimary"
                                                    href={
                                                        "/admin/delete/" +
                                                        post.slug
                                                    }
                                                    className={classes.link}
                                                >
                                                    <DeleteForeverIcon
                                                        key={(i + 1) * Math.random()}
                                                    ></DeleteForeverIcon>
                                                </Link>
                                            </TableCell>
                                        </TableRow>
                                    );
                                })}
                                <TableRow>
                                    <TableCell colSpan={4} align="right">
                                        <Button
                                            href={"/admin/create"}
                                            variant="contained"
                                            color="primary"
                                        >
                                            New Post
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            </TableBody>
                        </Table>
                    </TableContainer>
                </Paper>
            </Container>
        </React.Fragment>
    );
};
export default Posts;
