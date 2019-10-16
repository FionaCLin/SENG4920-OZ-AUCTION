import os, glob, re, collections, subprocess, random, csv, json, requests
from flask import Flask, render_template, session, request, redirect, url_for, Response


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
token = None



if __name__ == '__main__':
    app.run(debug =True)


