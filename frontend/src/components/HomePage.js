import React, { Component } from "react";
import CreateRoomPage from "./CreateRoomPage";
import RoomJoinPage from "./RoomJoinPage";
import Room from "./Room";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    Redirect,
} from "react-router-dom";
import { Grid, Typography, Button, ButtonGroup } from "@material-ui/core";

export default class HomePage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            roomCode: null,
        };

        this.removeRoomCode = this.removeRoomCode.bind(this);
    }

    async componentDidMount() {
        fetch("/bkd/user/room")
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                this.setState({
                    roomCode: data.code,
                });
            });
    }

    removeRoomCode() {
        this.setState({
            roomCode: null,
        });
    }

    renderHomePage() {
        return (
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <Typography component="h2" variant="h2">
                        Welcome to Music Rooms!
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <ButtonGroup variant="container" color="primary">
                        <Button
                            color="primary"
                            variant="contained"
                            to="/create"
                            component={Link}
                        >
                            Create a Room
                        </Button>
                        <Button
                            color="secondary"
                            variant="contained"
                            to="/join"
                            component={Link}
                        >
                            Join a Room
                        </Button>
                    </ButtonGroup>
                </Grid>
            </Grid>
        );
    }

    render() {
        return (
            <Router>
                <Switch>
                    <Route
                        exact
                        path="/"
                        render={() => {
                            return this.state.roomCode ? (
                                <Redirect to={`/room/${this.state.roomCode}`} />
                            ) : (
                                this.renderHomePage()
                            );
                        }}
                    />
                    <Route path="/join" component={RoomJoinPage} />
                    <Route path="/create" component={CreateRoomPage} />
                    <Route
                        path="/room/:roomCode"
                        render={(props) => {
                            return (
                                <Room
                                    {...props}
                                    leaveRoomCallbak={this.removeRoomCode}
                                />
                            );
                        }}
                    />
                </Switch>
            </Router>
        );
    }
}
