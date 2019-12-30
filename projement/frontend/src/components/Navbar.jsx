import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const Navbar = () => {
    return <nav className="navbar navbar-expand-md navbar-dark bg-primary mb-4">
        <div className="container">
            <a className="navbar-brand"
               href="/dashboard">Projement</a>
            <button className="navbar-toggler" type="button"
                    data-toggle="collapse" data-target="#navbar"
                    aria-controls="navbar" aria-expanded="false"
                    aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbar">
                <ul className="navbar-nav mr-auto">
                    <li className="nav-item">
                        <a className="nav-link"
                           href="/dashboard">Dashboard</a>
                    </li>
                </ul>
                <ul className="navbar-nav">
                    <li className="nav-item">
                        <a className="nav-link"
                           href="">Assignment</a>
                    </li>
                    <li className="nav-item dropdown">
                        <a className="nav-link dropdown-toggle" href="#"
                           id="dropdown"
                           data-toggle="dropdown" aria-haspopup="true"
                           aria-expanded="false">

                        </a>
                        <div className="dropdown-menu dropdown-menu-right"
                             aria-labelledby="dropdown">
                            <a className="dropdown-item"
                               href="">Admin</a>
                            <a className="dropdown-item"
                               href="">Log out</a>
                        </div>
                    </li>
                    <li className="nav-item">
                        <a className="nav-link" href="">Log
                            in</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

};

export default Navbar;