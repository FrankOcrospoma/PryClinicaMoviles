from flask import Flask, Blueprint, redirect, request, jsonify, render_template
from conexion import obtener_conexion

main = Blueprint("informeCitas", __name__, url_prefix="/informeCitas")