# Nova Boosting community

This repository contains what was an ongoing project for Nova Boosting Community (In world of warcraft).
They wanted a system to replace their mega sized google spreadsheet to track, distribute and calculate where billions of ingame gold coins were going.
The system tracked a players current wallet, transactiosn done between different wallets, payments, deductions and so on.

In addition it integrates with Raider.IO to verify skill and class for the players that wanted to become boosters.

In this repo there are 4 projects,

* NovaApi which is the API written in python, with FastAPI.
* NovaElectronApp which is a desktop client for the managers to micromanage the economy
* NovaFrontend which is where players would register, view their wallet and sign up for boosts
* NovaProject was the start of a ASP.NET rewrite of the API

Parallell to this a Discord bot was written by someone else, that would integrate with my API