from models.__init__ import SerializerMixin, validates, re, db

class Production(db.Model, SerializerMixin):
    __tablename__ = "productions"

    __table_args__ = (
        db.CheckConstraint("budget >= 0 AND budget < 1000000", name="check_positive_budget_less_than_one_million"),
        db.UniqueConstraint("title", "director", name="uq_title_per_director"),
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column("title", db.String(80), nullable=False, unique=True)
    genre = db.Column(db.String, nullable=False)
    director = db.Column(db.String)
    description = db.Column(db.String)
    budget = db.Column(db.Float)
    image = db.Column(db.String)
    ongoing = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    crew_members = db.relationship("CrewMember", back_populates="production", cascade="all, delete-orphan")
    creator = db.relationship("User", back_populates="created_productions")
    #! The following two lines are equivalent
    # serialize_only = ("id", "title", "genre", "director", "description", "budget", "image", "ongoing")
    serialize_rules = ("-crew_members", "-creator.created_productions")

    def __repr__(self):
        return f"""
            <Production #{self.id}:
                Title: {self.title}
                Genre: {self.genre}
                Director: {self.director}
                Description: {self.description}
                Budget: {self.budget}
                Image: {self.image}
                Ongoing: {self.ongoing}
            />
        """

    @validates("title", "director")
    def validate_title_and_director(self, attr_name, attr_value):
        if not isinstance(attr_value, str):
            raise TypeError(f"{attr_name} must be of type str")
        elif len(attr_value) < 1:
            raise ValueError(f"{attr_name} must be at least 1 characters long")
        else:
            return attr_value

    @validates("genre")
    def validate_genre(self, _, genre):  #! _ is a placeholder
        if not isinstance(genre, str):
            raise TypeError(f"Genre must be of type str")
        elif genre not in ["Drama", "Musical", "Opera"]:
            raise ValueError("Genre must be one of Musical, Opera or Drama")
        else:
            return genre

    @validates("description")
    def validate_description(self, _, description):
        if not isinstance(description, str):
            raise TypeError("Descriptions must be strings")
        elif len(description) < 10:
            raise ValueError(
                "description has to be a string of at least 10 characters"
            )
        return description

    @validates("budget")
    def validate_budget(self, _, budget):
        if type(budget) not in [int, float]:
            raise TypeError("Budgets must be numbers")
        elif budget not in range(0, 1000001):
            raise ValueError(f"{budget} has to be a positive float under 10Millions")
        return budget

    @validates("image")
    def validate_image(self, _, image):
        if not isinstance(image, str):
            raise TypeError("Images must be strings")
        elif not re.match(r"^https?:\/\/.*\.(?:png|jpeg|jpg)$", image):
            raise ValueError(
                f"{image} has to be a string of a valid url ending in png, jpeg or jpg"
            )
        return image

    @validates("ongoing")
    def validate_ongoing(self, _, ongoing):
        if not isinstance(ongoing, bool):
            raise TypeError(f"{ongoing} has to be a boolean")
        return ongoing
