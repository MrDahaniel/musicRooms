import React, { Component } from "react";

import { Grid, Button, Typography } from "@material-ui/core";

export default class Room extends Component {
    constructor(props) {
        super(props);
        this.state = {
            votesToSkip: 2,
            guestCanPause: false,
            isHost: false,
        };
        this.roomCode = this.props.match.params.roomCode;

        this.getRoomDetails = this.getRoomDetails.bind(this);
        this.getRoomDetails();

        this.leaveButtonClicked = this.leaveButtonClicked.bind(this);
    }

    getRoomDetails() {
        fetch("/bkd/get/room" + "?code=" + this.roomCode)
            .then((response) => {
                if (!response.ok) {
                    this.props.leaveRoomCallbak();
                    this.props.history.push("/");
                }

                return response.json();
            })
            .then((data) =>
                this.setState({
                    votesToSkip: data.votes_to_skip,
                    guestCanPause: data.guest_can_pause,
                    isHost: data.is_host,
                })
            );
    }

    leaveButtonClicked() {
        const requestOptions = {
            method: "POST",
            headers: { "Content-type": "application/json" },
            body: JSON.stringify({}),
        };

        fetch("/bkd/leave/room", requestOptions).then((_response) => {
            this.props.leaveRoomCallbak();
            this.props.history.push("/");
        });
    }

    render() {
        return (
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <Typography variant="h3" component="h3">
                        Code: {this.roomCode}
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <Typography variant="h5" component="h5">
                        Votes: {this.state.votesToSkip}
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <Typography variant="h5" component="h5">
                        Guest Can Pause: {this.state.guestCanPause.toString()}
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <Typography variant="h5" component="h5">
                        Is host: {this.state.isHost.toString()}
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button
                        color="secondary"
                        variant="contained"
                        onClick={this.leaveButtonClicked}
                    >
                        Return
                    </Button>
                </Grid>
            </Grid>
        );
    }
}
